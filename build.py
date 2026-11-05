"""Build stiiizy-portal.html (artifact, with vendor names) and docs/index.html (public, names stripped)."""
import json, re, copy, base64, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
src = open("portal_template.html").read()
loc = json.load(open("locations.json"))
seed = [dict(json.load(open(f"seed/WO-2610-{i:03d}.json")), id=f"WO-2610-{i:03d}") for i in range(1, 10)]
b64 = lambda f: base64.b64encode(open(f, "rb").read()).decode()
LOGO = {"__LOGO_LOCKUP__": b64("logo-lockup.png"), "__LOGO_ICON__": b64("logo-icon.png")}
def build(locs, sd, out, wrap=False):
    html = src.replace("__LOCATIONS__", json.dumps(locs, separators=(",", ":"))).replace("__SEED__", json.dumps(sd, separators=(",", ":")))
    for k, v in LOGO.items(): html = html.replace(k, v)
    for ph in ["__LOCATIONS__", "__SEED__", "__LOGO_LOCKUP__", "__LOGO_ICON__"]: assert ph not in html, ph
    if wrap:
        html = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
                '<style>:root{color-scheme:light}body{margin:0;font:14px system-ui}img{max-width:100%}[hidden]{display:none!important}</style></head><body>' + html + '</body></html>')
    open(out, "w").write(html); return html
h = build(loc, seed, "stiiizy-portal.html")
open("/private/tmp/claude-501/-Users-irfanzaman-Claude/317ec881-97f2-40c9-9327-e9a0eb85a1d0/scratchpad/portal_check.js", "w").write(re.search(r"<script>(.*)</script>", h, re.S).group(1))
pub = [dict(l, vendor=("Prime PM vendor" if l["vendor"] else "")) for l in loc]
sd = copy.deepcopy(seed)
for d in sd:
    if d.get("vendor"): d["vendor"] = "Prime PM vendor"
    if d.get("routing", {}).get("awardedVendor"): d["routing"]["awardedVendor"] = "Prime PM vendor"
    for hh in d.get("history", []):
        if " at $" in hh["note"]: hh["note"] = re.sub(r"^.* at \$", "Prime PM vendor at $", hh["note"])
g = build(pub, sd, "docs/index.html", wrap=True)
assert "Kyle Reimer" not in g
print("artifact", len(h), "bytes; public", len(g), "bytes")
