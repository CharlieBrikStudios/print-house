"""Pull every embedded base64 image out of the source page into v2/assets/img/<name>.webp."""
import os, re, base64, io, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); V2 = os.path.dirname(HERE)
seen = {}
for src in (f"{HERE}/src/index.html", f"{HERE}/src/andy/index.html"):
    s = open(src, encoding="utf-8").read()
    for m in re.finditer(r'--([a-zA-Z0-9_]+):url\((?:"|\')?data:image/([a-z+\-]+);base64,([A-Za-z0-9+/=]+)(?:"|\')?\)', s):
        name, kind, b64 = m.groups()
        out = f"{V2}/assets/img/{name}.webp"
        if name in seen and seen[name] == len(b64): continue
        if name in seen: print("differs between pages:", name)
        seen[name] = len(b64)
        raw = base64.b64decode(b64)
        if "svg" in kind:
            open(out.replace(".webp", ".svg"), "wb").write(raw); print("svg", name); continue
        im = Image.open(io.BytesIO(raw))
        lossless = im.mode in ("RGBA", "LA", "P") and kind == "png"
        if im.mode == "P": im = im.convert("RGBA")
        im.save(out, "WEBP", quality=86, lossless=False, method=6) if not lossless else im.save(out, "WEBP", quality=90, method=6)
print(len(seen), "images")
