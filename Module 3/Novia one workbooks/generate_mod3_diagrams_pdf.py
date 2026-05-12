"""Compile all Module 3 diagrams onto ONE landscape page (2x2 grid), in source-book order."""
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Image, Table, TableStyle,
)
from PIL import Image as PILImage
import os

OUTPUT = r"C:\Users\SuhaylO'Brien\OneDrive - BrickField Canvas\Documents\NOVIA ONE\Module 3\FMP Module 3 - Diagrams.pdf"
DIAG   = r"C:\Users\SuhaylO'Brien\OneDrive - BrickField Canvas\Documents\NOVIA ONE\Module 3\diagrams"

NAVY   = colors.HexColor("#121338")
ORANGE = colors.HexColor("#D4471A")
MUTED  = colors.HexColor("#555555")
TEXT   = colors.HexColor("#1A1A1A")
SOFT   = colors.HexColor("#F6F6FA")

PAGE_W, PAGE_H = landscape(A4)   # 842 x 595 pt   ≈ 297mm x 210mm
HEADER_H = 12 * mm
FOOTER_H = 10 * mm
M_TOP    = HEADER_H + 6 * mm
M_BOTTOM = FOOTER_H + 4 * mm
M_LEFT   = 14 * mm
M_RIGHT  = 14 * mm
GUTTER   = 6 * mm

TITLE = "FMP MODULE 3 — REGULATION OF FINANCIAL MARKETS"
SUB   = "Diagram Pack | Novia One"
STUDENT = "Suhayl O'Brien — NQF 7 Financial Markets Practitioner"


def header_footer(canv, doc):
    canv.saveState()
    canv.setFillColor(ORANGE)
    canv.rect(0, PAGE_H - HEADER_H, 30 * mm, HEADER_H, fill=1, stroke=0)
    canv.setFillColor(NAVY)
    canv.rect(30 * mm, PAGE_H - HEADER_H, PAGE_W - 30 * mm, HEADER_H, fill=1, stroke=0)
    canv.setFillColor(colors.white)
    canv.setFont("Helvetica-Bold", 9)
    canv.drawString(M_LEFT, PAGE_H - HEADER_H + 4 * mm, TITLE)
    canv.setFont("Helvetica", 8.5)
    canv.drawRightString(PAGE_W - M_RIGHT, PAGE_H - HEADER_H + 4 * mm, SUB)
    canv.setFillColor(NAVY)
    canv.rect(0, 0, PAGE_W, FOOTER_H, fill=1, stroke=0)
    canv.setFillColor(colors.white)
    canv.setFont("Helvetica", 8)
    canv.drawString(M_LEFT, 3.5 * mm, STUDENT)
    canv.drawRightString(PAGE_W - M_RIGHT, 3.5 * mm, f"Page {doc.page}")
    canv.restoreState()


CELL_TITLE = ParagraphStyle("CT", fontName="Helvetica-Bold", fontSize=10,
                             textColor=NAVY, leading=12, spaceAfter=2, alignment=1)
CELL_SECT  = ParagraphStyle("CS", fontName="Helvetica-Bold", fontSize=8,
                             textColor=ORANGE, leading=10, spaceAfter=2, alignment=1)
PAGE_TITLE = ParagraphStyle("PT", fontName="Helvetica-Bold", fontSize=14,
                             textColor=NAVY, leading=16, spaceAfter=6, alignment=0)
PAGE_INTRO = ParagraphStyle("PI", fontName="Helvetica", fontSize=8.5,
                             textColor=MUTED, leading=11, spaceAfter=6, alignment=0)


def fit_image(name, max_w, max_h):
    """Return an Image scaled to fit within max_w x max_h preserving aspect."""
    path = os.path.join(DIAG, name)
    im = PILImage.open(path)
    aspect = im.height / im.width
    target_w = max_w
    target_h = max_w * aspect
    if target_h > max_h:
        target_h = max_h
        target_w = target_h / aspect
    img = Image(path, width=target_w, height=target_h)
    img.hAlign = "CENTER"
    return img


def cell(section, title, name, max_w, max_h):
    """Build a stacked block: section label + title + image."""
    inner = [
        [Paragraph(section, CELL_SECT)],
        [Paragraph(title, CELL_TITLE)],
        [fit_image(name, max_w - 6, max_h)],
    ]
    t = Table(inner, colWidths=[max_w])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), SOFT),
        ("BOX", (0, 0), (-1, -1), 0.4, colors.HexColor("#DCDCDC")),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


def build():
    doc = BaseDocTemplate(
        OUTPUT, pagesize=landscape(A4),
        leftMargin=M_LEFT, rightMargin=M_RIGHT,
        topMargin=M_TOP, bottomMargin=M_BOTTOM,
        title="FMP Module 3 — Diagrams",
        author="Suhayl O'Brien",
    )
    frame = Frame(M_LEFT, M_BOTTOM,
                  PAGE_W - M_LEFT - M_RIGHT, PAGE_H - M_TOP - M_BOTTOM,
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
                  showBoundary=0)
    doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=header_footer)])

    s = []
    s.append(Paragraph("Regulation of Financial Markets — Diagram Pack", PAGE_TITLE))
    s.append(Paragraph(
        "All four core diagrams from the Module 3 study guide on a single page, in the order they appear in the source material "
        "(Ch 1.4.6 → Ch 2 → Ch 2.3 → Ch 3.3).",
        PAGE_INTRO))

    # Compute cell dimensions for 2x2 grid
    usable_w = PAGE_W - M_LEFT - M_RIGHT
    usable_h = PAGE_H - M_TOP - M_BOTTOM - 18 * mm  # leave room for title + intro
    cell_w   = (usable_w - GUTTER) / 2
    cell_h   = (usable_h - GUTTER) / 2
    img_max_h = cell_h - 14 * mm   # room for section + title

    # Diagrams in study-guide order
    blocks = [
        ("CHAPTER 1.4.6 · AML / CFT", "AML / CFT Regulatory Hierarchy",                    "aml_hierarchy.png"),
        ("CHAPTER 2 · SA Regulators", "South African Financial Regulatory Architecture", "sa_regulators.png"),
        ("CHAPTER 2.3 · Twin Peaks",  "South Africa's Twin Peaks Model",                  "twin_peaks.png"),
        ("CHAPTER 3.3 · Reg 28",      "Pension Funds Act, Reg 28 — Asset Class Caps",     "reg28_caps.png"),
    ]
    grid_rows = [
        [cell(*blocks[0], max_w=cell_w, max_h=cell_h),
         cell(*blocks[1], max_w=cell_w, max_h=cell_h)],
        [cell(*blocks[2], max_w=cell_w, max_h=cell_h),
         cell(*blocks[3], max_w=cell_w, max_h=cell_h)],
    ]
    grid = Table(grid_rows,
                 colWidths=[cell_w, cell_w],
                 rowHeights=[cell_h, cell_h])
    grid.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING",  (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    s.append(grid)

    doc.build(s)
    print("Wrote:", OUTPUT)


if __name__ == "__main__":
    build()
