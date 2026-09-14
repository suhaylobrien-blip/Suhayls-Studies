"""
Build the Module 7 study PDFs in the SA Bullion / Treasury-Brain house style.

Renders each HTML with headless Edge (@page margin:0 + explicit .sheet pages),
then VERIFIES:
  - rendered page count == number of .sheet divs (a mismatch means a sheet overflowed)
  - no .sheet is empty (a bad split leaves a section bar and a footer on a blank page,
    which the page count alone will NOT catch)
  - the top-left corner of every page is paper (#F4F3EE), never white
and writes page PNGs to build/snapshots/ for eyeballing.

Usage:  python build.py
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

import fitz  # PyMuPDF

HERE = os.path.dirname(os.path.abspath(__file__))
MOD = os.path.dirname(HERE)

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(EDGE):
    EDGE = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

PAPER = (244, 242, 237)  # #F4F3EE as Chromium renders it into the PDF

JOBS = [
    (
        "mod7-summary.html",
        os.path.join(MOD, "Summarised work book",
                     "Module 7 — Foreign Exchange Markets (Summarised Reference).pdf"),
    ),
    (
        "mod7-workbook.html",
        os.path.join(MOD, "Full in depth study material",
                     "Module 7 — Foreign Exchange Markets (In-Depth Workbook).pdf"),
    ),
    (
        "mod7-workbook-answers.html",
        os.path.join(MOD, "assignment",
                     "Module 7 — Foreign Exchange Markets (Workbook Answers).pdf"),
    ),
]


def sheet_count(html_path):
    with open(html_path, encoding="utf-8") as fh:
        return len(re.findall(r'<section class="sheet', fh.read()))


def empty_sheets(html_path):
    """Sheet numbers whose only content is the section bar and the footer."""
    with open(html_path, encoding="utf-8") as fh:
        html = fh.read()
    bad = []
    for i, sec in enumerate(re.findall(r'<section class="sheet.*?</section>', html, re.S), 1):
        body = re.sub(r'<div class="sec">.*?</div>', "", sec, flags=re.S)
        body = re.sub(r'<div class="foot">.*?</div>', "", body, flags=re.S)
        if not re.sub(r"<[^>]+>", " ", body).split():
            bad.append(i)
    return bad


def render(html_path, pdf_path):
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    profile = tempfile.mkdtemp(prefix="edgepdf-")
    try:
        subprocess.run(
            [
                EDGE,
                "--headless=new",
                "--disable-gpu",
                "--no-pdf-header-footer",
                f"--user-data-dir={profile}",
                f"--print-to-pdf={pdf_path}",
                "file:///" + html_path.replace("\\", "/"),
            ],
            check=True,
            timeout=300,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    finally:
        shutil.rmtree(profile, ignore_errors=True)


def verify(pdf_path, expected_sheets, snap_dir):
    doc = fitz.open(pdf_path)
    ok = True
    if doc.page_count != expected_sheets:
        print(f"  !! {doc.page_count} rendered pages vs {expected_sheets} sheets "
              f"— a sheet overflowed, split it")
        ok = False
    os.makedirs(snap_dir, exist_ok=True)
    for i, page in enumerate(doc, start=1):
        pix = page.get_pixmap(dpi=96)
        corner = pix.pixel(3, 3)
        if corner[:3] != PAPER:
            print(f"  !! page {i} corner {corner[:3]} is not paper {PAPER}")
            ok = False
        pix.save(os.path.join(snap_dir, f"p{i:02d}.png"))
    doc.close()
    return ok


def main():
    all_ok = True
    for html_name, pdf_path in JOBS:
        html_path = os.path.join(HERE, html_name)
        if not os.path.exists(html_path):
            print(f"{html_name}: missing, skipped")
            continue
        sheets = sheet_count(html_path)
        print(f"{html_name}: {sheets} sheets -> {os.path.basename(pdf_path)}")
        blanks = empty_sheets(html_path)
        if blanks:
            print(f"  !! sheets {blanks} are empty - a split left a blank page, remove them")
            all_ok = False
        render(html_path, pdf_path)
        snap_dir = os.path.join(HERE, "snapshots", html_name.replace(".html", ""))
        if verify(pdf_path, sheets, snap_dir):
            print("  ok")
        else:
            all_ok = False
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
