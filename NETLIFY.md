# Publish Orbit on Netlify

The deployable site is in netlify-site/. orbit-netlify.zip contains the same files.
It runs text retrieval in the browser with no API keys or Python server.
The CNN remains local and is explicitly unavailable in this online demo.

1. Open https://app.netlify.com/drop and sign in to your Netlify account.
2. Drop orbit-netlify.zip onto the page (or drop the netlify-site folder).
3. Netlify provides the live URL.

For updates, run python -B build_netlify.py, then upload the ZIP on your existing
project's Deploys page. Use the existing project to retain its URL.
Do not upload the whole Python project.

For a Git-connected deploy, commit netlify-site and netlify.toml, leave the build
command empty, and set the publish directory to netlify-site.
After editing chatbot.py, index.html, or astronomy-browser.js, rebuild and commit
the generated files too.

The original local application still runs with python app.py.
