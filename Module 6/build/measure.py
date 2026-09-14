"""One render, tagged sheets: report how many physical pages each .sheet takes."""
import os, re, shutil, subprocess, sys, tempfile
import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(EDGE):
    EDGE = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

src = sys.argv[1] if len(sys.argv) > 1 else "mod6-summary.html"
html = open(os.path.join(HERE, src), encoding="utf-8").read()

n = [0]
def tag(m):
    n[0] += 1
    return m.group(0) + f'<div style="font-size:6pt;color:#F4F3EE">ZQSHEET{n[0]:02d}ZQ</div>'
tagged = re.sub(r'<section class="sheet[^>]*>', tag, html)
total = n[0]

tmp = tempfile.mkdtemp(prefix="measure-")
shutil.copy(os.path.join(HERE, "pdf-house-style.css"), tmp)
hp = os.path.join(tmp, "t.html")
open(hp, "w", encoding="utf-8").write(tagged)
pdf = os.path.join(tmp, "t.pdf")
prof = tempfile.mkdtemp(prefix="edgep-")
subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                f"--user-data-dir={prof}", f"--print-to-pdf={pdf}",
                "file:///" + hp.replace("\\", "/")],
               check=True, timeout=300, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
shutil.rmtree(prof, ignore_errors=True)

doc = fitz.open(pdf)
starts = {}
for i, page in enumerate(doc, 1):
    for m in re.finditer(r"ZQSHEET(\d\d)ZQ", page.get_text()):
        s = int(m.group(1))
        starts.setdefault(s, i)
doc.close()

titles = re.findall(r'<section class="sheet.*?(?:class="sec">(.*?)<|>)', html, re.S)
secs = re.findall(r'<section class="sheet.*?</section>', html, re.S)
print(f"{src}: {total} sheets -> {len(fitz.open(pdf)) if False else ''}")
bad = []
for s in range(1, total + 1):
    a = starts.get(s)
    b = starts.get(s + 1, None)
    span = (b - a) if b else None
    t = re.search(r'class="sec">(.*?)<', secs[s-1])
    label = t.group(1)[:50] if t else "COVER"
    if span is None:
        print(f"  sheet {s:02d}: starts p{a} (last)")
    else:
        print(f"  sheet {s:02d}: {span} page(s)  {label}" + (f"   <-- OVERFLOWS by {span-1}" if span > 1 else ""))
        if span > 1:
            bad.append(s)
shutil.rmtree(tmp, ignore_errors=True)
print("overflowing sheets:", bad or "none")
