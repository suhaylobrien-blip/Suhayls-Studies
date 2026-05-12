"""Generate condensed Module 3 study summary PDF — Module 1/2 style."""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    FrameBreak, Image,
)

DIAG_DIR = r"C:\Users\SuhaylO'Brien\OneDrive - BrickField Canvas\Documents\NOVIA ONE\Module 3\diagrams"

OUTPUT = r"C:\Users\SuhaylO'Brien\OneDrive - BrickField Canvas\Documents\NOVIA ONE\Module 3\FMP Module 3 - Condensed Study Summary.pdf"

NAVY      = colors.HexColor("#121338")
ORANGE    = colors.HexColor("#D4471A")
GREY_BG   = colors.HexColor("#F2F2F2")
RULE      = colors.HexColor("#CCCCCC")
TEXT      = colors.HexColor("#1A1A1A")
MUTED     = colors.HexColor("#555555")
CALLOUT_BG = colors.HexColor("#FFF3E6")

PAGE_W, PAGE_H = A4
HEADER_H  = 12 * mm
FOOTER_H  = 10 * mm
M_TOP     = HEADER_H + 6 * mm
M_BOTTOM  = FOOTER_H + 4 * mm
M_LEFT    = 12 * mm
M_RIGHT   = 12 * mm
GUTTER    = 7 * mm

PAGE_TITLE = "FMP MODULE 3 — REGULATION OF FINANCIAL MARKETS"
SUBTITLE   = "Condensed Study Summary | Novia One"
STUDENT    = "Suhayl O'Brien — NQF 7 Financial Markets Practitioner"


def header_footer(canv, doc):
    canv.saveState()
    canv.setFillColor(ORANGE)
    canv.rect(0, PAGE_H - HEADER_H, 28 * mm, HEADER_H, fill=1, stroke=0)
    canv.setFillColor(NAVY)
    canv.rect(28 * mm, PAGE_H - HEADER_H, PAGE_W - 28 * mm, HEADER_H, fill=1, stroke=0)
    canv.setFillColor(colors.white)
    canv.setFont("Helvetica-Bold", 8.5)
    canv.drawString(M_LEFT, PAGE_H - HEADER_H + 4 * mm, PAGE_TITLE)
    canv.setFont("Helvetica", 8)
    canv.drawRightString(PAGE_W - M_RIGHT, PAGE_H - HEADER_H + 4 * mm, SUBTITLE)
    canv.setFillColor(NAVY)
    canv.rect(0, 0, PAGE_W, FOOTER_H, fill=1, stroke=0)
    canv.setFillColor(colors.white)
    canv.setFont("Helvetica", 8)
    canv.drawString(M_LEFT, 3.5 * mm, STUDENT)
    canv.drawRightString(PAGE_W - M_RIGHT, 3.5 * mm, f"Page {doc.page}")
    canv.restoreState()


H1 = ParagraphStyle("H1", fontName="Helvetica-Bold", fontSize=10.5, textColor=colors.white,
                    leading=13, backColor=NAVY, borderPadding=(4, 8, 4, 8),
                    spaceBefore=6, spaceAfter=6)
H2 = ParagraphStyle("H2", fontName="Helvetica-Bold", fontSize=9.2, textColor=NAVY,
                    leading=12, spaceBefore=5, spaceAfter=3)
BODY = ParagraphStyle("B", fontName="Helvetica", fontSize=8.6, textColor=TEXT,
                      leading=11.5, spaceAfter=3.5)
BULLET = ParagraphStyle("BU", fontName="Helvetica", fontSize=8.6, textColor=TEXT,
                        leading=11.5, leftIndent=11, bulletIndent=2, spaceAfter=2.5)
CALL_TITLE = ParagraphStyle("CT", fontName="Helvetica-Bold", fontSize=8.5,
                            textColor=ORANGE, leading=11.5, spaceAfter=3)
CALL_BODY = ParagraphStyle("CB", fontName="Helvetica", fontSize=8.6, textColor=TEXT,
                           leading=11.5, spaceAfter=2)
CELL = ParagraphStyle("CELL", fontName="Helvetica", fontSize=8.4, textColor=TEXT,
                      leading=11, spaceAfter=0)
CELL_B = ParagraphStyle("CELLB", fontName="Helvetica-Bold", fontSize=8.4,
                        textColor=colors.white, leading=11, spaceAfter=0)


def hsection(text): return Paragraph(text, H1)
def sub(text): return Paragraph(text, H2)
def p(text): return Paragraph(text, BODY)
def bul(items): return [Paragraph(f"<font color='#D4471A'>»</font> {i}", BULLET) for i in items]


def diagram(name, width):
    """Embed an image scaled to a target width, preserving aspect ratio."""
    import os
    from PIL import Image as PILImage
    path = os.path.join(DIAG_DIR, name)
    im = PILImage.open(path)
    aspect = im.height / im.width
    return Image(path, width=width, height=width * aspect)


def caption(text):
    return Paragraph(
        text,
        ParagraphStyle("cap", fontName="Helvetica-Oblique", fontSize=7.8,
                       textColor=MUTED, leading=10, alignment=1, spaceAfter=6)
    )


def callout(title, body_lines):
    rows = [[Paragraph(title, CALL_TITLE)]] + [[Paragraph(line, CALL_BODY)] for line in body_lines]
    t = Table(rows, colWidths=["100%"])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CALLOUT_BG),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LINEBEFORE", (0, 0), (0, -1), 2, ORANGE),
    ]))
    return t


def tbl(headers, rows, col_widths):
    header_row = [Paragraph(f"<b>{h}</b>", CELL_B) for h in headers]
    body_rows = [[Paragraph(c, CELL) for c in r] for r in rows]
    t = Table([header_row] + body_rows, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, GREY_BG]),
        ("LINEBELOW", (0, 0), (-1, 0), 0.4, NAVY),
        ("BOX", (0, 0), (-1, -1), 0.3, RULE),
        ("INNERGRID", (0, 1), (-1, -1), 0.2, RULE),
    ]))
    return t


def build():
    doc = BaseDocTemplate(
        OUTPUT, pagesize=A4,
        leftMargin=M_LEFT, rightMargin=M_RIGHT,
        topMargin=M_TOP, bottomMargin=M_BOTTOM,
        title="FMP Module 3 — Condensed Study Summary",
        author="Suhayl O'Brien",
    )
    fw = (PAGE_W - M_LEFT - M_RIGHT - GUTTER) / 2
    fh = PAGE_H - M_TOP - M_BOTTOM
    L = Frame(M_LEFT, M_BOTTOM, fw, fh, leftPadding=0, rightPadding=0,
              topPadding=0, bottomPadding=0, showBoundary=0)
    R = Frame(M_LEFT + fw + GUTTER, M_BOTTOM, fw, fh, leftPadding=0,
              rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
    doc.addPageTemplates([PageTemplate(id="t", frames=[L, R], onPage=header_footer)])

    s = []

    # ==================== PAGE 1 LEFT ====================
    s.append(hsection("CHAPTER 1 · FINANCIAL MARKETS REGULATION"))
    s.append(p("Effective markets need <b>legal certainty</b> and rules that protect against systemic failure, market manipulation and unfair treatment. The <b>Global Financial Crisis (2008)</b> exposed how lightly-regulated sub-prime lending in the US created systemic shocks worldwide — and why <b>conduct</b>, not just prudential, regulation now matters."))

    s.append(sub("1.2 Objectives of Regulation"))
    s.extend(bul([
        "<b>Protect consumers</b> — from abusive or manipulative products and fraud.",
        "<b>Foster capital formation &amp; growth</b> — channel savings to productive use.",
        "<b>Support economic stability</b> — prevent contagion across the system.",
        "<b>Ensure fairness</b> — address information asymmetry; prohibit insider trading.",
        "<b>Enhance efficiency</b> — standardise documentation &amp; processes.",
        "<b>Improve society</b> — AML / CFT, financial inclusion, environmental and social objectives.",
        "<b>Market confidence &amp; financial stability</b>; <b>reduce financial crime</b>; <b>regulate foreign participation</b>.",
    ]))

    s.append(sub("1.3 Consequences of Regulatory Failure"))
    s.extend(bul([
        "Reputational damage &amp; loss of trust in the system.",
        "Legal action — lawsuits and enforcement penalties.",
        "Business interruption &amp; loss of revenue.",
        "Worker injury / death, property damage, lost production (where physical operations are affected).",
        "Jail time, fines, limits on permitted activities.",
        "Reduced industry standards; market access issues.",
    ]))

    # ==================== PAGE 1 RIGHT ====================
    s.append(FrameBreak())

    s.append(sub("1.4 Types of Financial Market Regulation"))
    s.append(tbl(
        ["Type", "Focus"],
        [["<b>Competition</b>",       "Price-fixing, collusion, abuse of dominance, mergers / cartels."],
         ["<b>Consumer Protection</b>","Fair value, disclosure, refunds, product safety."],
         ["<b>Financial Sector</b>",  "Licensing, capital, conduct, reporting."],
         ["<b>Securities &amp; Exchange</b>", "Listing rules, insider trading, disclosure."],
         ["<b>Other sectors</b>",     "Telecoms / media, environment, labour, energy, food."]],
        col_widths=[fw * 0.30, fw * 0.70]
    ))

    s.append(sub("1.4.1 Gatekeeping Rules"))
    s.extend(bul([
        "<b>Personnel screening</b> — fit-and-proper checks on directors, advisors, key staff.",
        "<b>Firms</b> — licensing &amp; authorisation hurdles before market entry.",
        "<b>Financial products</b> — pre-approval &amp; suitability rules before sale to the public.",
    ]))

    s.append(sub("1.4.2 Operational Rules"))
    s.extend(bul([
        "<b>Internal controls</b> — segregation of duties, approvals, asset custody.",
        "<b>Risk management</b> — exposure limits, stress testing, capital adequacy.",
        "<b>Compliance &amp; ethics</b> — codes of conduct, conflicts management.",
        "<b>Technology &amp; resilience</b> — cyber, business continuity, system reliability.",
    ]))

    s.append(sub("1.4.3 Disclosure Rules"))
    s.append(p("Issuers must disclose material information — financial statements, governance, related-party deals — so investors can make informed choices."))

    # ==================== PAGE 2 LEFT ====================
    s.append(FrameBreak())

    s.append(sub("1.4.4 Sales Practice Rules"))
    s.extend(bul([
        "<b>Suitability</b> — the product must fit the client's risk profile &amp; needs.",
        "<b>Truthful advertising</b>; no misleading claims.",
        "Restrictions on <b>cold calling</b> &amp; aggressive sales tactics.",
        "<b>Mandatory disclosures</b>; complaint mechanisms; customer due diligence.",
    ]))

    s.append(sub("1.4.5 Trading Rules"))
    s.extend(bul([
        "<b>Best execution</b> — obtain the best reasonably available terms for the client.",
        "Trading time, place and frequency limits; transparency rules.",
        "Anti-manipulation: spoofing, layering, wash trades — all prohibited.",
    ]))

    s.append(sub("Proxy Voting Rules"))
    s.append(p("Define how shareholders authorise others to vote on their behalf. Cover eligibility, solicitation, voting mechanisms, instruction validity, deadlines, record-keeping and disclosure."))

    s.append(sub("1.4.6 AML / CFT Rules"))
    s.extend(bul([
        "<b>FICA</b> — SA's Financial Intelligence Centre Act, the local AML framework.",
        "<b>FATF</b> — Financial Action Task Force, sets the global AML standard.",
        "<b>ESAAMLG</b> — Eastern &amp; Southern African Anti-Money Laundering Group, the regional FATF body.",
    ]))
    s.append(diagram("aml_hierarchy.png", fw))
    s.append(caption("How global AML rules cascade into SA law and the FIC."))

    s.append(sub("1.4.7 Business Continuity Planning (BCP)"))
    s.append(p("Identify critical functions, document key processes, test recovery, train staff. Must be ready for natural disasters, pandemics, cyber-attacks &amp; tech failures."))

    s.append(callout("MEMORISE · GFC drives the regulatory agenda",
        ["The post-2008 mantra: <b>capital + conduct + transparency</b>. Almost every Mod 3 piece of legislation traces back to GFC lessons."]))

    # ==================== PAGE 2 RIGHT ====================
    s.append(FrameBreak())

    s.append(hsection("CHAPTER 2 · SOUTH AFRICAN REGULATORS"))
    s.append(p("SA adopted the <b>Twin Peaks</b> regulatory model under the <b>Financial Sector Regulation Act (FSRA) 9 of 2017</b>, effective 1 April 2018."))

    s.append(diagram("twin_peaks.png", fw))
    s.append(caption("Twin Peaks — one peak for safety, one peak for fairness."))

    s.append(sub("The Two Peaks"))
    s.append(tbl(
        ["Peak", "Body", "Role"],
        [["<b>Prudential</b>", "<b>Prudential Authority</b> (within SARB)",
          "Safety &amp; soundness of banks, insurers, market infrastructures."],
         ["<b>Conduct</b>",   "<b>FSCA</b> (Financial Sector Conduct Authority)",
          "Treating customers fairly, market integrity, fair pricing &amp; disclosure."]],
        col_widths=[fw * 0.20, fw * 0.30, fw * 0.50]
    ))

    s.append(sub("2.2.1 SARB — Reserve Bank"))
    s.extend(bul([
        "<b>Monetary policy</b> — inflation targeting in the 3–6% band (4.5% midpoint).",
        "<b>Currency stability</b> &amp; issuer of banknotes and coin.",
        "<b>Financial stability</b> — supervises banking sector via the Prudential Authority.",
        "<b>Foreign reserves</b>; <b>banker to government</b>; operates the <b>national payment system</b>.",
        "<b>Constitutionally independent</b> (s224 of the Constitution).",
    ]))

    s.append(sub("2.2.2 FSCA — Conduct Authority"))
    s.extend(bul([
        "Replaced the FSB in 2018 under FSRA.",
        "Supervises <b>market conduct</b> across banks, insurers, retirement funds, asset managers, advisors and exchanges.",
        "Enforces <b>Treating Customers Fairly (TCF)</b>; investigates misconduct; runs financial-literacy programmes.",
    ]))

    # ==================== PAGE 3 LEFT ====================
    s.append(FrameBreak())

    s.append(sub("2.2.3 NCR — National Credit Regulator"))
    s.extend(bul([
        "Established by the <b>National Credit Act (NCA)</b>.",
        "Registers credit providers, debt counsellors, credit bureaux.",
        "Combats reckless lending and over-indebtedness; promotes consumer credit education.",
        "Enforces affordability assessments and pricing disclosures.",
    ]))

    s.append(sub("2.2.4 JSE Limited"))
    s.extend(bul([
        "Africa's full-service securities exchange, <b>founded 1887</b>; top-20 globally by market cap.",
        "<b>Markets:</b> equity, bonds, derivatives, commodities, ETPs.",
        "<b>Self-regulating organisation (SRO)</b> — frontline regulator for listed entities under FSCA oversight.",
        "Sets <b>Listing Requirements</b>, runs surveillance &amp; enforcement, protects investors.",
    ]))

    s.append(sub("Other key role-players"))
    s.append(tbl(
        ["Body", "Role"],
        [["<b>National Treasury</b>", "Fiscal policy, budget, public finance, debt management."],
         ["<b>FIC</b>",               "Financial Intelligence Centre — AML / CFT operational hub."],
         ["<b>PASA</b>",              "Payments Association — oversees national payment system."],
         ["<b>NCR</b>",               "Credit industry regulator."],
         ["<b>CMS</b>",               "Council for Medical Schemes (medical aid)."]],
        col_widths=[fw * 0.30, fw * 0.70]
    ))

    s.append(sub("2.4 National Treasury — Functions"))
    s.extend(bul([
        "<b>Fiscal policy management</b> &amp; budget preparation.",
        "<b>Revenue collection oversight</b> (via SARS) &amp; expenditure control.",
        "<b>Public debt management</b> — sovereign bond issuance.",
        "<b>Intergovernmental finance</b> — provincial &amp; municipal allocations.",
        "<b>Public sector reform, anti-corruption &amp; development finance</b>.",
    ]))

    # ==================== PAGE 3 RIGHT ====================
    s.append(FrameBreak())

    s.append(hsection("CHAPTER 3 · SA LEGISLATION"))

    s.append(sub("3.1 Financial Sector Regulation Act — FSRA (Act 9 of 2017)"))
    s.append(p("Cornerstone act that established <b>Twin Peaks</b>. Creates the <b>Prudential Authority</b> &amp; <b>FSCA</b>, mandates co-operation between regulators, designates Systemically Important Financial Institutions (SIFIs), and provides for cross-border supervision and information-sharing."))

    s.append(sub("3.2 Collective Investment Schemes Control Act — CISCA (Act 45 of 2002)"))
    s.extend(bul([
        "Governs <b>unit trusts &amp; other CIS</b> — open- and closed-ended funds, hedge funds, property funds.",
        "Sets rules for <b>fund managers, trustees / custodians, administrators</b>.",
        "Investor protection through licensing, oversight, diversification &amp; liquidity limits.",
        "<b>FSCA</b> is the primary regulator; the manager and trustee/custodian are <b>independent</b>.",
    ]))

    s.append(sub("ASISA Standard on Fund Classification"))
    s.extend(bul([
        "Standardises how funds are categorised (asset allocation, geography, risk profile).",
        "Helps investors compare funds &amp; understand risk; eases regulatory reporting.",
        "Promotes <b>consistency, transparency &amp; standardisation</b> across the SA fund industry.",
    ]))

    s.append(sub("3.3 Pension Funds Act — Regulation 28"))
    s.append(p("Limits exposure of retirement funds to specific asset classes — protects members from concentration risk."))
    s.append(diagram("reg28_caps.png", fw))
    s.append(caption("Reg 28 — equities cap at 75% is the headline number to remember."))
    s.append(p("Reg 28 also encourages <b>Socially Responsible Investment (SRI)</b> — funds must consider ESG factors in long-term sustainability of returns."))

    # ==================== PAGE 4 LEFT ====================
    s.append(FrameBreak())

    s.append(sub("3.4 FAIS — Financial Advisory &amp; Intermediary Services Act (Act 37 of 2002)"))
    s.extend(bul([
        "Regulates <b>Financial Services Providers (FSPs)</b> and their representatives.",
        "<b>Licensing</b> required by FSCA before giving advice / intermediary services.",
        "<b>Fit-and-proper requirements:</b> personal character, honesty, qualifications, experience, operational competence, financial soundness.",
        "<b>Categories of FSPs</b> — Cat I (advice on most products) through Cat IV (Trust &amp; Company services).",
        "Mandatory <b>disclosure</b>, <b>record-keeping</b> &amp; <b>complaints procedures</b>.",
        "FAIS Ombud handles consumer disputes.",
    ]))

    s.append(sub("3.5 FICA — Financial Intelligence Centre Act (Act 38 of 2001)"))
    s.extend(bul([
        "Establishes the <b>Financial Intelligence Centre (FIC)</b> — SA's AML/CFT hub.",
        "<b>Accountable institutions</b> must register with FIC and apply <b>Customer Due Diligence (CDD) / KYC</b>.",
        "<b>Suspicious Transaction Reports (STRs)</b> &amp; <b>Cash Threshold Reports</b> filed with FIC.",
        "Risk-based approach; <b>Risk Management &amp; Compliance Programme (RMCP)</b> required.",
        "Penalties include administrative fines, criminal prosecution and licence revocation.",
    ]))

    s.append(sub("3.6 POPIA — Protection of Personal Information Act (Act 4 of 2013)"))
    s.extend(bul([
        "Safeguards <b>personal information</b> from unauthorised access, use or disclosure.",
        "Governs how info is <b>collected, processed, stored and shared</b>.",
        "Requires <b>transparency, accountability</b> and appointment of an <b>Information Officer</b>.",
        "Enforced by the <b>Information Regulator</b>; fines up to R10m and criminal liability.",
    ]))

    s.append(callout("EXAM FOCUS · Three Letters Every FMP Must Know",
        ["<b>FSRA</b> → built Twin Peaks (PA + FSCA).",
         "<b>FAIS</b> → licenses advisors &amp; sets fit-and-proper.",
         "<b>FICA</b> → AML / KYC and the FIC."]))

    # ==================== PAGE 4 RIGHT ====================
    s.append(FrameBreak())

    s.append(hsection("CHAPTER 4 · INTERNATIONAL REGULATIONS"))

    s.append(sub("4.1 Dodd-Frank Act (USA, 2010)"))
    s.extend(bul([
        "Post-GFC US reform — full name: Dodd-Frank Wall Street Reform and Consumer Protection Act.",
        "<b>Volcker Rule:</b> bans deposit-taking banks from proprietary trading with depositor funds.",
        "Created the <b>Consumer Financial Protection Bureau (CFPB)</b>.",
        "Brings <b>OTC derivatives</b> &amp; hedge funds into regulatory daylight via central clearing &amp; reporting.",
        "Oversees credit-rating agencies (Moody's, S&amp;P, Fitch).",
        "Impact on SA: any SA institution dealing with US counterparties / markets must comply.",
    ]))

    s.append(sub("4.2 Basel III (Solvency)"))
    s.append(p("International accord developed by the <b>Basel Committee on Banking Supervision (BCBS)</b> in response to the GFC. Strengthens bank capital, liquidity and leverage."))
    s.append(tbl(
        ["Element", "Definition"],
        [["<b>Capital ratios</b>",
          "Higher quantity &amp; quality of Tier 1 capital."],
         ["<b>LCR</b>",
          "Liquidity Coverage Ratio — survive 30-day liquidity stress."],
         ["<b>NSFR</b>",
          "Net Stable Funding Ratio — match long-term assets with stable funding."],
         ["<b>Leverage ratio</b>",
          "Non-risk-based backstop on total exposures."]],
        col_widths=[fw * 0.30, fw * 0.70]
    ))
    s.append(p("Endorsed by the G20; implemented in SA by SARB / Prudential Authority."))

    s.append(sub("4.3 EMIR — European Market Infrastructure Regulation"))
    s.extend(bul([
        "EU rules adopted in 2012 covering <b>OTC derivatives</b>.",
        "Requires <b>reporting</b> of all derivative trades to trade repositories.",
        "Mandates <b>central clearing</b> for standardised OTC derivatives via CCPs.",
        "Imposes <b>risk-mitigation techniques</b> for non-cleared trades (margining, confirmation, reconciliation).",
        "ESMA supervises trade repositories.",
    ]))

    s.append(sub("4.4 FATCA — Foreign Account Tax Compliance Act (US)"))
    s.extend(bul([
        "US law to <b>combat offshore tax evasion</b> by US persons.",
        "SA signed an <b>IGA with the IRS</b> in 2014 — SA banks &amp; FSPs report US account-holders to SARS, which forwards to the IRS.",
        "Promotes the automatic exchange of tax information across borders.",
    ]))

    # ==================== PAGE 5 LEFT ====================
    s.append(FrameBreak())

    s.append(hsection("RAPID RECAP · WHO REGULATES WHAT"))
    s.append(tbl(
        ["Body", "Statute", "Mandate"],
        [["<b>SARB</b>",     "SA Reserve Bank Act / Constitution s224",
          "Monetary policy, currency, financial stability, banker to government."],
         ["<b>PA</b>",       "FSRA 9 / 2017",
          "Prudential supervision — banks, insurers, market infrastructures."],
         ["<b>FSCA</b>",     "FSRA 9 / 2017",
          "Market conduct — fair treatment of customers, market integrity."],
         ["<b>NCR</b>",      "National Credit Act 34 / 2005",
          "Consumer credit — registration, reckless lending, debt counselling."],
         ["<b>FIC</b>",      "FICA 38 / 2001",
          "AML / CFT — STRs, CTRs, accountable-institution oversight."],
         ["<b>Info Reg.</b>","POPIA 4 / 2013",
          "Personal information protection &amp; data privacy."],
         ["<b>JSE</b>",      "Financial Markets Act 19 / 2012",
          "Self-regulatory exchange; listings, surveillance, enforcement."],
         ["<b>Treasury</b>", "Public Finance Mgmt Act 1 / 1999",
          "Fiscal policy, budgets, public debt, intergovernmental finance."],
         ["<b>Comp. Comm</b>","Competition Act 89 / 1998",
          "Anti-collusion, abuse of dominance, merger control."]],
        col_widths=[fw * 0.20, fw * 0.32, fw * 0.48]
    ))

    s.append(callout("EXAM FOCUS · Twin Peaks in one line",
        ["<b>Prudential Authority = safety of the institution.</b> <b>FSCA = fairness to the customer.</b> Same financial firm typically reports to both."]))

    # ==================== PAGE 5 RIGHT ====================
    s.append(FrameBreak())

    s.append(hsection("KEY ACRONYMS"))
    s.append(tbl(
        ["Acronym", "Meaning"],
        [["<b>FSRA</b>",     "Financial Sector Regulation Act 9 of 2017 — created Twin Peaks"],
         ["<b>PA</b>",       "Prudential Authority — within SARB"],
         ["<b>FSCA</b>",     "Financial Sector Conduct Authority — successor to FSB"],
         ["<b>SARB</b>",     "South African Reserve Bank"],
         ["<b>NCR</b>",      "National Credit Regulator"],
         ["<b>FIC / FICA</b>","Financial Intelligence Centre / FIC Act 38 of 2001 — AML"],
         ["<b>FATF</b>",     "Financial Action Task Force — global AML standard-setter"],
         ["<b>ESAAMLG</b>",  "Eastern &amp; Southern African AML Group — regional FATF body"],
         ["<b>FAIS</b>",     "Financial Advisory &amp; Intermediary Services Act 37 of 2002"],
         ["<b>FSP</b>",      "Financial Services Provider — licensed under FAIS"],
         ["<b>CISCA</b>",    "Collective Investment Schemes Control Act 45 of 2002"],
         ["<b>ASISA</b>",    "Association for Savings &amp; Investment SA — industry body"],
         ["<b>Reg 28</b>",   "Pension Funds Act regulation — asset class limits"],
         ["<b>POPIA</b>",    "Protection of Personal Information Act 4 of 2013"],
         ["<b>STR / CTR</b>","Suspicious Transaction Report / Cash Threshold Report"],
         ["<b>KYC / CDD</b>","Know Your Customer / Customer Due Diligence"],
         ["<b>RMCP</b>",     "Risk Management &amp; Compliance Programme — FICA"],
         ["<b>SIFI</b>",     "Systemically Important Financial Institution"],
         ["<b>TCF</b>",      "Treating Customers Fairly — FSCA framework"],
         ["<b>BCP</b>",      "Business Continuity Planning"],
         ["<b>Dodd-Frank</b>","US 2010 post-GFC reform incl. Volcker Rule, CFPB"],
         ["<b>Basel III</b>","BCBS bank capital, liquidity &amp; leverage standards"],
         ["<b>EMIR</b>",     "European Market Infrastructure Regulation — OTC derivatives"],
         ["<b>FATCA</b>",    "US Foreign Account Tax Compliance Act — IGA with SARS"],
         ["<b>JSE</b>",      "Johannesburg Stock Exchange — frontline SRO"],
         ["<b>SRO</b>",      "Self-Regulating Organisation"]],
        col_widths=[fw * 0.24, fw * 0.76]
    ))

    doc.build(s)
    print("Wrote:", OUTPUT)


if __name__ == "__main__":
    build()
