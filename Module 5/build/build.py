"""
Build the Module 5 study PDFs in the SA Bullion / Treasury-Brain house style.

Renders each HTML with headless Edge (@page margin:0 + explicit .sheet pages),
then VERIFIES:
  - rendered page count == number of .sheet divs (a mismatch means a sheet overflowed)
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
        "mod5-summary.html",
        os.path.join(MOD, "Summarised work book",
                     "Module 5 — Interest Bearing Securities & Bonds (Summarised Reference).pdf"),
    ),
    (
        "mod5-workbook.html",
        os.path.join(MOD, "Full in depth study material",
                     "Module 5 — Interest Bearing Securities & Bonds (In-Depth Workbook).pdf"),
    ),
]


def sheet_count(html_path):
    with open(html_path, encoding="utf-8") as fh:
        return len(re.findall(r'<section class="sheet', fh.read()))


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
        render(html_path, pdf_path)
        snap_dir = os.path.join(HERE, "snapshots", html_name.replace(".html", ""))
        if verify(pdf_path, sheets, snap_dir):
            print("  ok")
        else:
            all_ok = False
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
