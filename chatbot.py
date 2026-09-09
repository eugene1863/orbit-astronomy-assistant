"""Small, transparent astronomy reference retriever (not a language model)."""
import re

TOPICS = [
    ("black holes", ["black hole", "black holes", "event horizon"],
     "A black hole is a region where gravity is so strong that light cannot escape from inside its event horizon. Some form when massive stars collapse. We detect them through their effects on nearby matter and light.",
     "https://science.nasa.gov/universe/black-holes/"),
    ("stars", ["star", "stars", "sun", "fusion"],
     "Stars are hot spheres of gas powered mainly by nuclear fusion in their cores. They form as clouds of gas collapse under gravity. A star's mass strongly influences its lifetime and how it ends its life. Our Sun is a star.",
     "https://science.nasa.gov/universe/stars/"),
    ("galaxies", ["galaxy", "galaxies", "milky way"],
     "A galaxy is a gravitationally bound system of stars, gas, dust, and dark matter. The Milky Way, our home galaxy, is a barred spiral. Galaxies have a wide range of sizes and shapes.",
     "https://science.nasa.gov/universe/galaxies/"),
    ("galaxy shapes", ["spiral", "elliptical", "irregular", "galaxy types", "galaxy shapes"],
     "Spiral galaxies have disks with spiral arms. Elliptical galaxies look rounded or elongated and generally contain older stars. Irregular galaxies lack a regular overall shape. These are the three broad labels used by this project's image classifier; real galaxy morphology is more varied.",
     "https://science.nasa.gov/universe/galaxies/types/"),
    ("planets", ["planet", "planets", "solar system"],
     "Our solar system has eight planets: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune. The inner four are rocky; Jupiter and Saturn are gas giants, while Uranus and Neptune are ice giants.",
     "https://science.nasa.gov/solar-system/planets/"),
    ("the Moon", ["moon", "lunar", "phases"],
     "The Moon is Earth's natural satellite. It reflects sunlight. As it orbits Earth, we see different portions of its sunlit half, producing lunar phases. Ordinary phases are not caused by Earth's shadow.",
     "https://science.nasa.gov/moon/"),
    ("light-years", ["light year", "light years", "lightyear", "lightyears"],
     "A light-year is a distance, not a duration: it is how far light travels in a vacuum in one year, about 9.46 trillion kilometers. Looking at distant objects means seeing light that left them in the past.",
     "https://spaceplace.nasa.gov/light-year/en/"),
    ("exoplanets", ["exoplanet", "exoplanets"],
     "An exoplanet is a planet outside our solar system. Astronomers can find some by measuring dips in a star's brightness during a transit, or by measuring how an orbiting planet makes its star wobble.",
     "https://science.nasa.gov/exoplanets/"),
    ("the Big Bang", ["big bang", "universe", "expansion"],
     "The Big Bang model describes the universe's expansion from an early hot, dense state. It is not an explosion from a central point into empty space; space itself expands. The model is supported by observations including the cosmic microwave background.",
     "https://science.nasa.gov/universe/overview/"),
    ("dark matter", ["dark matter"],
     "Dark matter is matter inferred from gravitational effects, including galaxy motions and gravitational lensing. It does not emit or absorb light in the way ordinary luminous matter does. Its physical nature remains unknown.",
     "https://science.nasa.gov/universe/dark-matter-dark-energy/"),
    ("supernovae", ["supernova", "supernovae", "exploding star"],
     "A supernova is a powerful stellar explosion. Some occur when massive stellar cores collapse; another major kind involves the thermonuclear destruction of a white dwarf. Supernovae help distribute elements into surrounding space.",
     "https://science.nasa.gov/universe/stars/"),
]
def answer(question):
    q = re.sub(r"[^a-z0-9 ]", " ", question.lower())
    q = " ".join(q.split())
    if q in {"hi", "hello", "hey"}:
        return {"answer": "Hello! Ask me about black holes, stars, galaxies, planets, the Moon, light-years, exoplanets, dark matter, or supernovae.", "sources": []}
    if any(word in q.split() for word in ("latest", "today", "current", "tonight")):
        return {"answer": "I don't have live astronomy news or observing conditions. Try a general astronomy question, or consult a current astronomy source.", "sources": []}
    ranked = []
    for title, aliases, body, url in TOPICS:
        score = max((len(alias.split()) * 10 + len(alias) for alias in aliases
                     if re.search(r"\b" + re.escape(alias) + r"\b", q)), default=0)
        if score:
            ranked.append((score, title, body, url))
    if not ranked:
        return {"answer": "I don't have a reliable answer in my small reference set yet. Try asking what a black hole is, how stars form, or about galaxy shapes.", "sources": []}
    ranked.sort(reverse=True)
    selected = ranked[:2] if any(w in q.split() for w in ("compare", "difference")) else ranked[:1]
    return {"answer": "\n\n".join(r[2] for r in selected),
            "sources": [{"title": r[1], "url": r[3]} for r in selected]}
