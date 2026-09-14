"""True overage per sheet: re-render with break-inside:avoid disabled so content
flows continuously, then the content on page 2 IS the amount the sheet is too tall by."""
import os, re, shutil, subprocess, sys, tempfile
import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(EDGE):
    EDGE = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
src = sys.argv[1] if len(sys.argv) > 1 else "mod7-summary.html"
html = open(os.path.join(HERE, src), encoding="utf-8").read()
n = [0]
def tag(m):
    n[0] += 1
    return m.group(0) + f'<div style="font-size:6pt;color:#F4F3EE">ZQSHEET{n[0]:02d}ZQ</div>'
tagged = re.sub(r'<section class="sheet[^>]*>', tag, html)
total = n[0]
tagged = tagged.replace("</head>",
    "<style>.card,.note,.def,.exam,table,.kv,.formula,.grid2>*,h3,h4{break-inside:auto!important}"
    "tr,td,th{break-inside:auto!important}</style></head>")
tmp = tempfile.mkdtemp(prefix="over-")
shutil.copy(os.path.join(HERE, "pdf-house-style.css"), tmp)
hp = os.path.join(tmp, "t.html"); open(hp, "w", encoding="utf-8").write(tagged)
pdf = os.path.join(tmp, "t.pdf"); prof = tempfile.mkdtemp(prefix="edgep-")
subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                f"--user-data-dir={prof}", f"--print-to-pdf={pdf}",
                "file:///" + hp.replace("\\", "/")], check=True, timeout=300,
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
shutil.rmtree(prof, ignore_errors=True)
doc = fitz.open(pdf)
starts = {}
for i, page in enumerate(doc, 1):
    for m in re.finditer(r"ZQSHEET(\d\d)ZQ", page.get_text()):
        starts.setdefault(int(m.group(1)), i)
secs = re.findall(r'<section class="sheet.*?</section>', html, re.S)
PT_MM = 25.4 / 72
worst = []
for s in range(1, total + 1):
    a = starts.get(s); b = starts.get(s + 1)
    span = (b - a) if b else (doc.page_count - a + 1)
    t = re.search(r'class="sec">(.*?)<', secs[s-1])
    label = (t.group(1) if t else "COVER")[:42]
    if span <= 1:
        continue
    page = doc[a + span - 2]
    blocks = [bl for bl in page.get_text("blocks") if bl[4].strip()
              and "ZQSHEET" not in bl[4] and "Novia One · FMP" not in bl[4]
              and "Summarised Reference" not in bl[4]]
    over = max((bl[3] for bl in blocks), default=0) * PT_MM
    # usable box is 297 - 16 top - 20 bottom = 261mm; page 2 content starts at 16mm top pad
    over = over - 16
    head = " ".join(sorted(blocks, key=lambda b: b[1])[0][4].split())[:58] if blocks else "(footer only)"
    worst.append((over, s, label, head))
for over, s, label, head in sorted(worst, reverse=True):
    print(f"sheet {s:02d}  ~{over:6.1f} mm over   {label}")
    print(f"            spills: {head}")
print(f"\n{len(worst)} of {total} sheets over. usable content box = 261 mm")
shutil.rmtree(tmp, ignore_errors=True)
