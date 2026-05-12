"""Build Module 3 Workbook Q&A PDF — questions verbatim + model answers from Modules 1-3."""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    KeepTogether,
)

OUTPUT = r"C:\Users\SuhaylO'Brien\OneDrive - BrickField Canvas\Documents\NOVIA ONE\Module 3\FMP Module 3 - Workbook Answers.pdf"

NAVY      = colors.HexColor("#121338")
ORANGE    = colors.HexColor("#D4471A")
GREEN_OK  = colors.HexColor("#1F6E3A")
GREY_BG   = colors.HexColor("#F2F2F2")
LIGHT_BG  = colors.HexColor("#F8F4ED")
QBOX_BG   = colors.HexColor("#EEF0F8")
RULE      = colors.HexColor("#CCCCCC")
TEXT      = colors.HexColor("#1A1A1A")
MUTED     = colors.HexColor("#555555")

PAGE_W, PAGE_H = A4
HEADER_H, FOOTER_H = 12 * mm, 10 * mm
M_TOP = HEADER_H + 6 * mm
M_BOTTOM = FOOTER_H + 4 * mm
M_LEFT, M_RIGHT = 16 * mm, 16 * mm

TITLE = "FMP MODULE 3 — WORKBOOK ANSWERS"
SUB = "Practical Evidence | Suhayl O'Brien"


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
    canv.drawString(M_LEFT, 3.5 * mm, "Suhayl O'Brien — NQF 7 Financial Markets Practitioner")
    canv.drawRightString(PAGE_W - M_RIGHT, 3.5 * mm, f"Page {doc.page}")
    canv.restoreState()


QH = ParagraphStyle("QH", fontName="Helvetica-Bold", fontSize=12, textColor=colors.white,
                    leading=14, backColor=NAVY, borderPadding=(4, 8, 4, 8),
                    spaceBefore=8, spaceAfter=6)
Q = ParagraphStyle("Q", fontName="Helvetica-Bold", fontSize=9.5, textColor=NAVY,
                   leading=12, spaceAfter=2)
QT = ParagraphStyle("QT", fontName="Helvetica", fontSize=9.5, textColor=TEXT,
                    leading=12, spaceAfter=4)
A_LABEL = ParagraphStyle("AL", fontName="Helvetica-Bold", fontSize=9, textColor=GREEN_OK,
                         leading=11, spaceAfter=2)
A_BODY = ParagraphStyle("A", fontName="Helvetica", fontSize=9, textColor=TEXT,
                        leading=12, spaceAfter=3)
BUL = ParagraphStyle("BUL", fontName="Helvetica", fontSize=9, textColor=TEXT,
                     leading=12, leftIndent=12, bulletIndent=2, spaceAfter=1)
MARK = ParagraphStyle("MK", fontName="Helvetica-Oblique", fontSize=8.5, textColor=MUTED,
                      leading=10)


def question_panel(qno, qtext, marks):
    t = Table(
        [[Paragraph(f"<b>{qno}</b>", Q),
          Paragraph(qtext, QT),
          Paragraph(f"<b>({marks})</b>", MARK)]],
        colWidths=[14 * mm, None, 14 * mm],
    )
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), QBOX_BG),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LINEBEFORE", (0, 0), (0, -1), 2, NAVY),
    ]))
    return t


def answer_panel(flow):
    rows = [[Paragraph("ANSWER", A_LABEL)]] + [[f] for f in flow]
    t = Table(rows, colWidths=["100%"])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BG),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, 0), 4),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 4),
        ("TOPPADDING", (0, 1), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 1),
        ("LINEBEFORE", (0, 0), (0, -1), 2, GREEN_OK),
    ]))
    return t


def b(items):
    return [Paragraph(f"<font color='#D4471A'>»</font> {i}", BUL) for i in items]


def qa(qno, qtext, marks, flow):
    return KeepTogether([
        question_panel(qno, qtext, marks),
        Spacer(1, 2),
        answer_panel(flow),
        Spacer(1, 6),
    ])


def section_title(t):
    return Paragraph(t, QH)


CELL_HEAD = ParagraphStyle("CELLH", fontName="Helvetica-Bold", fontSize=9,
                           textColor=colors.white, leading=11, spaceAfter=0)
CELL_BODY = ParagraphStyle("CELLB", fontName="Helvetica", fontSize=9,
                           textColor=TEXT, leading=11, spaceAfter=0)


def tbl(headers, rows, col_widths):
    """Wrap every cell in a Paragraph so &lt;b&gt; HTML tags render."""
    header_row = [Paragraph(h, CELL_HEAD) for h in headers]
    body_rows = [[Paragraph(c, CELL_BODY) for c in r] for r in rows]
    data = [header_row] + body_rows
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, GREY_BG]),
        ("BOX", (0, 0), (-1, -1), 0.4, RULE),
        ("INNERGRID", (0, 1), (-1, -1), 0.2, RULE),
    ]))
    return t


def build():
    doc = BaseDocTemplate(
        OUTPUT, pagesize=A4,
        leftMargin=M_LEFT, rightMargin=M_RIGHT,
        topMargin=M_TOP, bottomMargin=M_BOTTOM,
        title="FMP Module 3 Workbook Answers",
        author="Suhayl O'Brien",
    )
    frame = Frame(M_LEFT, M_BOTTOM,
                  PAGE_W - M_LEFT - M_RIGHT, PAGE_H - M_TOP - M_BOTTOM,
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
                  showBoundary=0)
    doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=header_footer)])

    s = []

    s.append(Paragraph(
        "FMP Module 3 — Regulation of Financial Markets: Workbook Answers",
        ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=18,
                       textColor=NAVY, leading=22, spaceAfter=6)
    ))
    s.append(Paragraph(
        "Each question is quoted verbatim from the workbook (V05, 25-05-19), followed "
        "by a model answer grounded in the Module 3 study guide (with cross-references "
        "to Modules 1 and 2 where useful). Total marks: 75. Pass mark: 65%.",
        ParagraphStyle("intro", fontName="Helvetica", fontSize=10,
                       textColor=MUTED, leading=14, spaceAfter=14)
    ))

    # ============================== Q1 [10] ==============================
    s.append(section_title("QUESTION 1 · Foundations of Regulation [10 marks]"))

    s.append(qa("1.1",
        "Discuss the role of regulation in maintaining financial stability in markets, "
        "with reference to the Global Financial Crisis (GFC) of 2008.", 2, [
        Paragraph("Regulation provides the <b>legal certainty, prudential safeguards and conduct "
                  "rules</b> that allow financial markets to function without collapsing on each other. "
                  "It reduces the risk of <b>systemic failure</b>, sets capital and liquidity buffers, "
                  "and limits market manipulation.", A_BODY),
        Paragraph("The <b>2008 GFC</b> is the textbook case: US banks repackaged sub-prime mortgages "
                  "into AAA-rated CDOs while regulators failed to see the build-up of leverage and "
                  "interconnected risk. When defaults rose, the contagion spread globally — Lehman "
                  "collapsed, money markets froze, and recession followed. The crisis catalysed the "
                  "wave of post-2008 reforms (Dodd-Frank, Basel III, EMIR and SA's own Twin Peaks model "
                  "via FSRA 2017) — all designed to push <b>capital, conduct, and transparency</b> back "
                  "into the system.", A_BODY),
    ]))

    s.append(qa("1.2",
        "Explain the broad objectives of financial market regulation and provide examples "
        "of how regulators achieve these objectives.", 2, [
        *b([
            "<b>Protect consumers</b> — e.g. FAIS licensing of advisors and FSCA's TCF programme.",
            "<b>Foster capital formation &amp; growth</b> — JSE listing requirements channel savings to issuers.",
            "<b>Support economic stability</b> — Basel III capital ratios under the Prudential Authority.",
            "<b>Ensure fairness</b> — JSE surveillance and insider-trading prohibitions in the Financial Markets Act.",
            "<b>Enhance efficiency</b> — STRATE dematerialisation; standardised reporting (FICA, EMIR).",
            "<b>Improve society</b> — FICA / FATF AML rules combat money-laundering and terror financing.",
        ]),
    ]))

    s.append(qa("1.3",
        "Analyse the consequences of regulatory failure in financial markets, citing potential "
        "impacts on customers, businesses, and the economy.", 2, [
        Paragraph("Regulatory failure cascades through three layers:", A_BODY),
        *b([
            "<b>Customers</b> — mis-selling, loss of savings, identity theft, eroded confidence in the financial system.",
            "<b>Businesses</b> — fines, criminal sanctions, reputational damage, loss of licences, business interruption, share-price impact.",
            "<b>Economy</b> — bank runs &amp; contagion, recessions (as per GFC), credit-rating downgrades, currency weakness, capital flight, taxpayer-funded bailouts.",
        ]),
    ]))

    s.append(qa("1.4",
        "Describe the importance of transparency and fairness in financial markets and the "
        "role of regulation in achieving these objectives.", 2, [
        Paragraph("Markets only work when participants <b>trust the price</b>. Transparency and "
                  "fairness:", A_BODY),
        *b([
            "Reduce <b>information asymmetry</b> between issuers and investors, and between dealers and clients.",
            "Allow accurate <b>price discovery</b> — the core economic function of any market.",
            "Underpin <b>investor confidence</b>, lowering the cost of capital for the real economy.",
        ]),
        Paragraph("Regulators deliver this through <b>mandatory disclosure</b> (issuer reporting, FAIS "
                  "advisor disclosures), <b>insider-trading prohibitions</b>, <b>best-execution</b> rules, "
                  "and <b>market surveillance</b> by SROs like the JSE and conduct authority FSCA.", A_BODY),
    ]))

    s.append(qa("1.5",
        "What are the key regulatory bodies in South Africa that oversee financial markets, "
        "and what are their primary functions?", 2, [
        tbl(
            ["Body", "Primary function"],
            [["<b>SARB</b> (incl. Prudential Authority)",
              "Monetary policy, currency, financial stability, prudential supervision of banks &amp; insurers."],
             ["<b>FSCA</b>", "Market conduct regulator — TCF, market integrity, consumer protection."],
             ["<b>NCR</b>",  "Consumer credit industry under the National Credit Act."],
             ["<b>FIC</b>",  "AML / CFT operational hub under FICA."],
             ["<b>JSE</b>",  "Frontline self-regulator of listed markets under the Financial Markets Act."],
             ["<b>Treasury</b>", "Fiscal policy, budget, public debt and intergovernmental finance."],
             ["<b>Info Regulator</b>", "POPIA — personal information &amp; data privacy."]],
            col_widths=[60 * mm, None]
        ),
    ]))

    # ============================== Q2 [15] ==============================
    s.append(section_title("QUESTION 2 · Gatekeeping, Operational &amp; Proxy Rules [15 marks]"))

    s.append(qa("2.1", "Discuss the role and importance of gatekeeping rules in financial markets.", 5, [
        Paragraph("Gatekeeping rules control <b>who is allowed into the market</b> and what products may "
                  "be offered. They cover three layers:", A_BODY),
        *b([
            "<b>Personnel screening</b> — fit-and-proper requirements for directors, advisors and key individuals (qualifications, honesty, financial soundness, operational competence).",
            "<b>Firms</b> — licensing and authorisation by the FSCA (FAIS Cat I–IV), Prudential Authority (banks, insurers), or SROs (JSE listing approval) before any market participation.",
            "<b>Products</b> — pre-approval of CIS portfolios under CISCA; suitability rules; restrictions on selling complex products to retail clients.",
        ]),
        Paragraph("<b>Importance:</b> they raise the entry bar so that bad actors are filtered out before "
                  "they can cause customer harm. They are the <b>first line of defence</b> against fraud, "
                  "mis-selling and systemic shocks, and they support the <b>integrity and credibility</b> "
                  "of the market as a whole — which lowers the cost of capital for legitimate issuers.",
                  A_BODY),
    ]))

    s.append(qa("2.2",
        "Explain the key components of operational rules within financial organisations and their significance.",
        5, [
        Paragraph("Operational rules govern how a regulated firm runs its day-to-day business. The "
                  "main components are:", A_BODY),
        *b([
            "<b>Internal controls</b> — segregation of duties, approval levels, custody of client assets, regular reconciliations.",
            "<b>Risk management</b> — exposure limits, capital adequacy, stress testing, asset / liability matching.",
            "<b>Compliance &amp; ethics</b> — codes of conduct, conflict-of-interest management, employee dealing rules.",
            "<b>Transaction handling</b> — trade affirmation, settlement discipline, error correction protocols.",
            "<b>Technology &amp; resilience</b> — cyber-security, business continuity planning, system reliability and data integrity.",
        ]),
        Paragraph("<b>Significance:</b> these rules turn high-level regulation into <b>concrete daily "
                  "behaviour</b>. Without them, even a well-licensed firm could fail catastrophically — "
                  "as several rogue trading scandals (Barings, Société Générale, Archegos) have "
                  "demonstrated. They protect customers, shareholders and the wider financial system.",
                  A_BODY),
    ]))

    s.append(qa("2.3",
        "What are the challenges and benefits of proxy voting rules in corporate governance?",
        5, [
        Paragraph("<b>Proxy voting rules</b> allow shareholders who cannot attend an AGM in person to "
                  "appoint someone to vote on their behalf. The rules cover eligibility, solicitation, "
                  "voting mechanisms, deadlines and disclosure.", A_BODY),
        Paragraph("<b>Benefits:</b>", A_BODY),
        *b([
            "Maximise shareholder participation — especially institutional investors holding shares for retail clients.",
            "Strengthen oversight of company management on remuneration, board composition and ESG matters.",
            "Lower the cost of corporate democracy — no need to physically attend every AGM.",
            "Improve accountability through publicly disclosed voting records.",
        ]),
        Paragraph("<b>Challenges:</b>", A_BODY),
        *b([
            "<b>Conflicts of interest</b> — asset managers may hesitate to vote against companies they want as banking clients.",
            "<b>Complexity</b> — resolutions can be technical; small shareholders may not understand the issues.",
            "Mismatch between <b>beneficial</b> owners (retail clients) and <b>registered</b> holders (custodians).",
            "Difficulty in <b>chasing instructions</b> from large numbers of fund members within tight deadlines.",
            "Risk of <b>robo-voting</b> where managers follow proxy-advisor recommendations without independent judgement.",
        ]),
    ]))

    # ============================== Q3 [15] ==============================
    s.append(section_title("QUESTION 3 · SARB, FSCA &amp; NCR [15 marks]"))

    s.append(qa("3.1", "What are the key roles and responsibilities of the South African Reserve Bank (SARB)?",
                5, [
        *b([
            "<b>Monetary policy</b> — set the repo rate to keep CPI within the <b>3–6% target band</b> (4.5% midpoint preferred); MPC meets six times per year.",
            "<b>Currency stability</b> — sole issuer of banknotes and coin; manages official gold and foreign-exchange reserves.",
            "<b>Financial stability</b> — supervises the banking sector through the <b>Prudential Authority</b> and acts as the macroprudential authority for the system as a whole.",
            "<b>National payment system</b> — operates SAMOS and oversees PASA; ensures safe, efficient settlement.",
            "<b>Banker to government</b> &amp; <b>lender of last resort</b> in liquidity crises; administers remaining exchange controls.",
        ]),
        Paragraph("Independence is <b>constitutionally entrenched (s224)</b>, with the primary objective "
                  "being to <b>protect the value of the currency in the interest of balanced and "
                  "sustainable economic growth</b>.", A_BODY),
    ]))

    s.append(qa("3.2",
        "How does the Financial Sector Conduct Authority (FSCA) contribute to market conduct "
        "regulation in South Africa?", 5, [
        Paragraph("The FSCA was established in 2018 under <b>FSRA 9 of 2017</b> as the conduct peak of "
                  "SA's Twin Peaks regulatory model, replacing the former FSB.", A_BODY),
        *b([
            "<b>Supervises market conduct</b> across banks, insurers, retirement funds, asset managers, advisors and exchanges.",
            "<b>Enforces Treating Customers Fairly (TCF)</b> outcomes — fair products, clear info, no mis-selling.",
            "<b>Investigates misconduct</b> — insider trading, market abuse, mis-selling, false advertising; imposes administrative penalties.",
            "<b>Licenses</b> FSPs under FAIS and approves CIS managers under CISCA.",
            "<b>Promotes financial literacy</b> and inclusion through education campaigns.",
            "<b>Co-operates internationally</b> via IOSCO and bilateral MoUs; shares supervisory information with PA and FIC.",
        ]),
    ]))

    s.append(qa("3.3",
        "What are the primary roles of the National Credit Regulator (NCR) in regulating "
        "South Africa's credit industry?", 5, [
        Paragraph("The NCR was established under the <b>National Credit Act (NCA) 34 of 2005</b> to "
                  "oversee the consumer credit market.", A_BODY),
        *b([
            "<b>Registration</b> of credit providers, credit bureaux, debt counsellors and payment distribution agents.",
            "<b>Reckless lending controls</b> — affordability assessments, credit-bureau enquiries before granting credit.",
            "<b>Consumer protection</b> — pricing disclosure, in-duplum rule (interest cap), debt counselling and debt review.",
            "<b>Enforcement &amp; investigations</b> — fines, deregistration and referral of criminal conduct to the National Consumer Tribunal.",
            "<b>Financial literacy</b> — consumer education on borrowing, credit reports and over-indebtedness.",
        ]),
    ]))

    # ============================== Q4 [17] ==============================
    s.append(section_title("QUESTION 4 · JSE and Twin Peaks Model [17 marks]"))

    s.append(qa("4.1",
        "What are the primary market functions and services provided by the Johannesburg Stock Exchange (JSE)?",
        5, [
        Paragraph("Founded in 1887, the JSE is Africa's full-service securities exchange and one of "
                  "the top-20 globally by market capitalisation. Its market functions are:", A_BODY),
        *b([
            "<b>Equity market</b> — Main Board &amp; AltX listings; primary issuance (IPOs / FPOs) and secondary trading.",
            "<b>Bond market</b> — government, parastatal and corporate debt; one of the deepest in EM.",
            "<b>Derivatives market</b> — equity, currency, interest-rate, agricultural and commodity derivatives via Safex / Yield-X.",
            "<b>Commodities</b> — physical and financial agri products (white maize, yellow maize, soya, wheat, sunflower).",
            "<b>ETPs / structured products</b> — ETFs, ETNs, AMCs.",
            "Provides <b>price discovery, liquidity and post-trade infrastructure</b> (clearing via JSE Clear, settlement via STRATE).",
        ]),
    ]))

    s.append(qa("4.2",
        "How does the Johannesburg Stock Exchange (JSE) contribute to market regulation and investor protection?",
        5, [
        Paragraph("The JSE is a <b>Self-Regulatory Organisation (SRO)</b> licensed under the "
                  "Financial Markets Act 19 of 2012 and supervised by the FSCA &amp; Prudential Authority.",
                  A_BODY),
        *b([
            "<b>Listing Requirements</b> — set minimum standards for issuers (free float, governance, financials, disclosure).",
            "<b>Surveillance</b> — real-time monitoring of trading for manipulation, insider trading and disorderly conduct.",
            "<b>Enforcement</b> — censures, fines and de-listings against issuers and members that breach rules; criminal cases referred to FSCA / NPA.",
            "<b>Trading rules</b> — best execution, transparency, market-maker obligations and circuit breakers.",
            "<b>Investor protection</b> — Continuing Obligations &amp; SENS announcements ensure timely price-sensitive disclosure; JSE Investor Protection Fund covers certain broker-default losses.",
        ]),
    ]))

    s.append(qa("4.3", "Explain the Twin Peaks regulatory model in South Africa.", 3, [
        Paragraph("Introduced by the <b>Financial Sector Regulation Act (FSRA) 9 of 2017</b>, effective "
                  "1 April 2018. The model splits financial regulation into two specialised "
                  "<b>peaks</b>:", A_BODY),
        *b([
            "<b>Prudential Authority (PA)</b> — housed within SARB, focuses on the <b>safety and soundness</b> of financial institutions.",
            "<b>Financial Sector Conduct Authority (FSCA)</b> — focuses on the <b>market conduct</b> of those same institutions toward customers and counterparties.",
            "Together they replaced the old <b>single-regulator (FSB)</b> approach, which the GFC showed to be inadequate for handling both prudential and conduct issues at the same firm.",
        ]),
    ]))

    s.append(qa("4.4", "Describe the role of the Prudential Authority in context of the Twin Peaks Model.", 2, [
        Paragraph("The PA — operating <b>within SARB</b> — ensures the <b>financial soundness</b> of banks, "
                  "insurers, market infrastructures and financial conglomerates. It sets and enforces "
                  "<b>capital, liquidity, leverage and risk-management</b> standards (Basel III for banks, "
                  "SAM for insurers), conducts on-site inspections and stress tests, and supervises "
                  "systemically important institutions to protect the stability of the financial system "
                  "as a whole.", A_BODY),
    ]))

    s.append(qa("4.5", "Describe the role of the FSCA in context of the Twin Peaks Model.", 2, [
        Paragraph("The FSCA is the <b>conduct peak</b> — focused on how regulated firms <b>treat their "
                  "customers</b> and behave in the market. It enforces <b>Treating Customers Fairly</b>, "
                  "polices market abuse and insider trading, licenses FSPs under FAIS, approves CIS "
                  "managers under CISCA, and works alongside the PA so the same firm faces consistent "
                  "supervision on both soundness and conduct.", A_BODY),
    ]))

    # ============================== Q5 [18] ==============================
    s.append(section_title("QUESTION 5 · ASISA, Regulation 28 &amp; Regulatory Objectives [18 marks]"))

    s.append(qa("5.1", "What is the primary purpose of the ASISA Standard on Fund Classification?", 3, [
        Paragraph("The ASISA Standard provides a <b>consistent industry-wide framework for classifying "
                  "Collective Investment Schemes</b>, so that investors and advisors can compare funds "
                  "on a like-for-like basis.", A_BODY),
        *b([
            "Sets clear categories based on <b>asset class, geography and risk profile</b> (e.g. SA Equity General, Global Multi-Asset High Equity).",
            "Reduces confusion from inconsistent or marketing-driven fund labels.",
            "Promotes <b>transparency, standardisation and comparability</b> across the SA fund industry.",
        ]),
    ]))

    s.append(qa("5.2", "How does Regulation 28 of the Pension Funds Act ensure the safety of pension fund investments?",
                3, [
        Paragraph("Reg 28 places <b>limits on how much of a retirement fund's assets can be exposed to "
                  "any one asset class or counterparty</b>. The goal is <b>diversification and risk "
                  "control</b> for members who depend on the fund for retirement income.", A_BODY),
        *b([
            "Caps exposure to equities, property, foreign assets, hedge funds, private equity and single counterparties.",
            "Enforces <b>concentration limits</b> at issuer and instrument level.",
            "Mandates ongoing monitoring and remedial action if limits are breached.",
            "Encourages a <b>long-term, well-diversified</b> portfolio that can meet pension obligations.",
        ]),
    ]))

    s.append(qa("5.3",
        "What is the maximum percentage of pension fund assets that can be invested in equities "
        "according to Regulation 28?", 3, [
        Paragraph("Under <b>Regulation 28 of the Pension Funds Act</b>, a retirement fund may not invest "
                  "more than <b>75% of its assets in equities</b> (listed and unlisted combined). For "
                  "context, the other key caps are:", A_BODY),
        tbl(
            ["Asset class", "Maximum exposure"],
            [["<b>Equities</b>",                          "<b>75%</b>"],
             ["Foreign (offshore) assets",                "45%"],
             ["Property",                                  "25%"],
             ["Private equity",                            "15%"],
             ["Hedge funds",                               "15%"],
             ["Single issuer (concentration limit)",       "Varies — typically 5–25% by credit quality"]],
            col_widths=[80 * mm, None]
        ),
        Paragraph("Cash and money market may be held up to 100% subject to liquidity needs.", A_BODY),
    ]))

    s.append(qa("5.4", "What is the role of socially responsible investment (SRI) in Regulation 28?", 3, [
        Paragraph("Regulation 28 explicitly requires retirement funds to <b>consider environmental, "
                  "social and governance (ESG) factors</b> in the long-term sustainability of investment "
                  "returns.", A_BODY),
        *b([
            "Funds must <b>consider</b> ESG risks when constructing portfolios — it is not an opt-in extra.",
            "Encourages allocation to <b>infrastructure, green energy and developmental investments</b> that benefit the broader economy.",
            "Aligns retirement-fund stewardship with the <b>Code for Responsible Investing in South Africa (CRISA)</b>.",
            "Recognises that <b>ignoring ESG risks (climate, governance failures) can destroy long-term value</b> for fund members.",
        ]),
    ]))

    s.append(qa("5.5", "How does the ASISA Standard on Fund Classification help improve transparency in the investment industry?",
                3, [
        *b([
            "<b>Consistent categories</b> mean any fund can be compared against true peers — no hiding behind creative naming.",
            "<b>Standardised disclosure</b> of asset allocation, geography and risk forces managers to describe what they actually do.",
            "Easier <b>regulatory reporting</b> — FSCA and trustees can monitor adherence to mandates.",
            "Reduces <b>misleading marketing</b> — investors get clearer information when choosing funds.",
            "Supports informed advice from <b>FAIS-licensed advisors</b> who must give suitable recommendations.",
        ]),
    ]))

    s.append(qa("5.6", "Explain the primary objective of financial market regulation.", 3, [
        Paragraph("The <b>primary objective</b> of financial market regulation is to <b>maintain a fair, "
                  "stable and efficient financial system that protects consumers and supports "
                  "sustainable economic growth</b>.", A_BODY),
        Paragraph("This single objective breaks down into the secondary aims covered in the FMP "
                  "study guide:", A_BODY),
        *b([
            "<b>Consumer protection</b> — against fraud, mis-selling and abusive practices.",
            "<b>Financial stability</b> — preventing systemic failures of the GFC type.",
            "<b>Market integrity</b> — fair and transparent price discovery.",
            "<b>Capital formation</b> — efficient channelling of savings to productive investment.",
            "<b>Financial inclusion &amp; social objectives</b> — AML / CFT, equitable access.",
        ]),
    ]))

    s.append(Spacer(1, 8))
    s.append(Paragraph(
        "<b>Total marks: 75</b> &nbsp;|&nbsp; Q1: 10 · Q2: 15 · Q3: 15 · Q4: 17 · Q5: 18 "
        "&nbsp;|&nbsp; Pass mark: 65% (49 marks)",
        ParagraphStyle("totals", fontName="Helvetica", fontSize=9, textColor=MUTED,
                       leading=12, alignment=1)
    ))

    doc.build(s)
    print("Wrote:", OUTPUT)


if __name__ == "__main__":
    build()
