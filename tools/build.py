"""Build both targets from one source.

src/page.html (fragment + /*__DATA__*/ marker), src/script.json and voice/*.mp3
-> index.html        full document for GitHub Pages
-> build/artifact.html  fragment for the Cowork preview (the platform adds doctype/head)
"""
import base64, json, pathlib, subprocess

root = pathlib.Path(__file__).resolve().parent.parent
page = (root / "src/page.html").read_text(encoding="utf-8")
script = json.loads((root / "src/script.json").read_text(encoding="utf-8"))

aud, dur = {}, {}
for lang in ("vi", "en"):
    aud[lang], dur[lang] = [], []
    for k in range(1, 7):
        f = root / f"voice/{lang}{k}.mp3"
        aud[lang].append("data:audio/mpeg;base64," + base64.b64encode(f.read_bytes()).decode())
        d = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)])
        dur[lang].append(round(float(d), 2))

data = ("var AUD=" + json.dumps(aud) + ";\nvar DUR=" + json.dumps(dur) +
        ";\nvar NARR=" + json.dumps(script, ensure_ascii=False) + ";")
assert page.count("/*__DATA__*/") == 1
fragment = page.replace("/*__DATA__*/", data)

(root / "build").mkdir(exist_ok=True)
(root / "build/artifact.html").write_text(fragment, encoding="utf-8")

head_end = fragment.index("</style>") + len("</style>")
doc = ('<!doctype html>\n<html lang="vi">\n<head>\n<meta charset="utf-8">\n'
       '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
       '<meta name="robots" content="noindex, nofollow">\n'
       '<style>body{margin:0}</style>\n'
       + fragment[:head_end] + "\n</head>\n<body>\n" + fragment[head_end:] + "\n</body>\n</html>\n")
(root / "index.html").write_text(doc, encoding="utf-8")
print("built", len(doc), "bytes; durations", dur)
