"""Build a standalone Netlify site from the local UI and reference topics."""
import json
import re
import zipfile
from pathlib import Path
from chatbot import TOPICS
ROOT = Path(__file__).resolve().parent
def main():
    target = ROOT / "netlify-site"
    target.mkdir(exist_ok=True)
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    html = html.replace("<script>", '<script src="astronomy.js"></script>\n<script>')
    html, count = re.subn(r"async function post\(path,data\)\{.*?\}\n",
        "async function post(path,data){if(path === '/api/chat')return astronomyAnswer(data.question);throw Error('Image classification requires the local Python app.');}\n", html)
    assert count == 1, "Could not locate API helper"
    html, count = re.subn(r"fetch\('/api/status'\).*?\n",
        "$('status').textContent='Image model unavailable online';$('result').textContent='This web demo answers text questions. Galaxy classification requires a trained model and the local Python app.';\n", html)
    assert count == 1, "Could not locate model status"
    html = html.replace('CNN training requires labeled images', 'Text demo · Image classification runs in the local Python app')
    (target / "index.html").write_text(html, encoding="utf-8")
    logic = (ROOT / "astronomy-browser.js").read_text(encoding="utf-8")
    (target / "astronomy.js").write_text("const TOPICS = " + json.dumps(TOPICS) + ";\n" + logic, encoding="utf-8")
    (target / "_headers").write_text("/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n", encoding="utf-8")
    with zipfile.ZipFile(ROOT / "orbit-netlify.zip", "w", zipfile.ZIP_DEFLATED) as archive:
        for name in ("index.html", "astronomy.js", "_headers"):
            archive.write(target / name, name)
    print("Built netlify-site and orbit-netlify.zip")
if __name__ == "__main__":
    main()
