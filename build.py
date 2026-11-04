"""Build one notes page per folder from its notes.txt, plus the home page. Run: python build.py

In notes.txt the first two lines are the title and the byline. Lines listed in HEADINGS become section headings,
and lines starting with a bullet become a list.
"""
import html
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
HEADINGS = {"Author's note", "AI disclosure", "Craft influences", "Image credits", "Fonts", "Trailer sound"}
HEAD = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{t}</title><meta name="description" content="{d}"><link href="https://fonts.googleapis.com/css2?family=Anton&family=Instrument+Serif&display=swap" rel="stylesheet"><link rel="stylesheet" href="{css}"></head><body><main>'


def link(s):
    return re.sub(r"(https?://[^\s]+)", r'<a href="\1">\1</a>', html.escape(s, quote=False))


items = []
for f in sorted(HERE.glob("*/notes.txt")):
    lines = f.read_text(encoding="utf-8").splitlines()
    title, by = lines[0], lines[1]
    out = [HEAD.format(t=html.escape(f"{title}: notes"), d=html.escape(f"Author's note, AI disclosure and credits for {title}, {by}."), css="../style.css"), f"<h1>{html.escape(title)}</h1><p class='by'>{html.escape(by)}</p>"]
    in_list = False
    for line in lines[2:]:
        line = line.strip()
        if not line:
            continue
        bullet = line.startswith("• ")
        if bullet and not in_list:
            out.append("<ul>")
        if not bullet and in_list:
            out.append("</ul>")
        in_list = bullet
        if bullet:
            out.append(f"<li>{link(line[2:])}</li>")
        elif line in HEADINGS:
            out.append(f"<h2>{html.escape(line)}</h2>")
        else:
            out.append(f"<p>{link(line)}</p>")
    if in_list:
        out.append("</ul>")
    out.append("</main></body></html>")
    (f.parent / "index.html").write_text("\n".join(out), encoding="utf-8")
    items.append(f'<li><a href="{f.parent.name}/">{html.escape(title)}</a></li>')
home = HEAD.format(t="Bryan Kwandou: novel notes", d="Author's notes, AI disclosures and credits for novels by Bryan Kwandou.", css="style.css") + "<h1>Bryan Kwandou</h1><p class='by'>Author's notes, AI disclosures and credits</p><ul>" + "".join(items) + "</ul></main></body></html>"
(HERE / "index.html").write_text(home, encoding="utf-8")
print("built", len(items))
