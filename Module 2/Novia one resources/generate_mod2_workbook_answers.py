"""Build Module 2 Workbook Q&A PDF — questions verbatim + model answers from Mod 1 & 2."""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    KeepTogether, PageBreak
)

OUTPUT = r"C:\Users\SuhaylO'Brien\OneDrive - BrickField Canvas\Documents\NOVIA ONE\Module 2\FMP Module 2 - Workbook Answers.pdf"

NAVY      = colors.HexColor("#121338")
ORANGE    = colors.HexColor("#D4471A")
GREEN_OK  = colors.HexColor("#1F6E3A")
GREY_BG   = colors.HexColor("#F2F2F2")
LIGHT_BG  = colors.HexColor("#F8F4ED")  # answer panel
QBOX_BG   = colors.HexColor("#EEF0F8")  # question panel
RULE      = colors.HexColor("#CCCCCC")
TEXT      = colors.HexColor("#1A1A1A")
MUTED     = colors.HexColor("#555555")

PAGE_W, PAGE_H = A4
HEADER_H, FOOTER_H = 12 * mm, 10 * mm
M_TOP = HEADER_H + 6 * mm
M_BOTTOM = FOOTER_H + 4 * mm
M_LEFT, M_RIGHT = 16 * mm, 16 * mm

TITLE = "FMP MODULE 2 — WORKBOOK ANSWERS"
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
QSUB = ParagraphStyle("QSUB", fontName="Helvetica-Bold", fontSize=10, textColor=NAVY,
                      leading=12, spaceBefore=4, spaceAfter=3)
Q = ParagraphStyle("Q", fontName="Helvetica-Bold", fontSize=9.5, textColor=NAVY,
                   leading=12, spaceAfter=2)
QT = ParagraphStyle("QT", fontName="Helvetica", fontSize=9.5, textColor=TEXT, leading=12,
                    spaceAfter=4)
A_LABEL = ParagraphStyle("AL", fontName="Helvetica-Bold", fontSize=9, textColor=GREEN_OK,
                         leading=11, spaceAfter=2)
A_BODY = ParagraphStyle("A", fontName="Helvetica", fontSize=9, textColor=TEXT, leading=12,
                        spaceAfter=3)
BUL = ParagraphStyle("BUL", fontName="Helvetica", fontSize=9, textColor=TEXT, leading=12,
                     leftIndent=12, bulletIndent=2, spaceAfter=1)
MARK = ParagraphStyle("MK", fontName="Helvetica-Oblique", fontSize=8.5, textColor=MUTED,
                      leading=10)


def q_block(qno, text, marks):
    return Table(
        [[Paragraph(f"<b>{qno}</b>", Q), Paragraph(text, QT),
          Paragraph(f"({marks})", MARK)]],
        colWidths=[14 * mm, None, 14 * mm],
    )


def question_panel(qno, qtext, marks):
    inner = Table(
        [[Paragraph(f"<b>{qno}</b>", Q),
          Paragraph(qtext, QT),
          Paragraph(f"<b>({marks})</b>", MARK)]],
        colWidths=[14 * mm, None, 14 * mm],
    )
    inner.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), QBOX_BG),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LINEBEFORE", (0, 0), (0, -1), 2, NAVY),
    ]))
    return inner


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


def section_title(t):
    return Paragraph(t, QH)


def qa(qno, qtext, marks, answer_flow):
    return KeepTogether([
        question_panel(qno, qtext, marks),
        Spacer(1, 2),
        answer_panel(answer_flow),
        Spacer(1, 6),
    ])


def small_table(headers, rows, col_widths):
    data = [headers] + rows
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
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
        title="FMP Module 2 Workbook Answers",
        author="Suhayl O'Brien",
    )
    frame = Frame(M_LEFT, M_BOTTOM,
                  PAGE_W - M_LEFT - M_RIGHT, PAGE_H - M_TOP - M_BOTTOM,
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
                  showBoundary=0)
    doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=header_footer)])

    s = []

    # ===================== INTRO =====================
    s.append(Paragraph(
        "FMP Module 2 — Fundamentals of Economics: Workbook Answers",
        ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=18,
                       textColor=NAVY, leading=22, spaceAfter=6)
    ))
    s.append(Paragraph(
        "Each question is quoted verbatim from the workbook (V06, 25-05-19), "
        "followed by a model answer grounded in the Module 1 and Module 2 study guides. "
        "Total marks: 110.",
        ParagraphStyle("intro", fontName="Helvetica", fontSize=10,
                       textColor=MUTED, leading=14, spaceAfter=14)
    ))

    # ===================== Q1 [15] =====================
    s.append(section_title("QUESTION 1 · Foundational Concepts [15 marks]"))

    s.append(qa("1.1",
        "What is the central concept in economics that explains the fundamental economic problem, "
        "and how does it affect decision-making?", 3, [
        Paragraph("<b>Scarcity</b> is the central concept of economics. It captures the fact that "
                  "human wants are unlimited while resources — money, time, labour, raw materials, "
                  "land — are finite.", A_BODY),
        *b([
            "Forces every actor (household, firm, government) to <b>choose</b> between competing uses.",
            "Every choice carries an <b>opportunity cost</b> — the value of the next-best alternative foregone.",
            "Drives the three core economic questions: <b>what</b> to produce, <b>how</b> to produce it, and <b>for whom</b>.",
        ]),
    ]))

    s.append(qa("1.2",
        "What is the difference between explicit costs and implicit costs in a company's "
        "financial analysis?", 3, [
        small_table(
            ["", "<b>Explicit costs</b>", "<b>Implicit costs</b>"],
            [["Cash exchange?", "Yes — actual outflows", "No cash changes hands"],
             ["Measurable?", "Yes — recorded in accounts", "Difficult to measure exactly"],
             ["Examples", "Wages, rent, raw materials, interest paid",
              "Owner's unpaid labour, interest foregone on own capital, opportunity cost of using own premises"]],
            col_widths=[28 * mm, 60 * mm, None]
        ),
        Spacer(1, 4),
        Paragraph("Accounting profit deducts only explicit costs; <b>economic profit</b> deducts both.", A_BODY),
    ]))

    s.append(qa("1.3",
        "How is opportunity cost calculated, and why is it important in economic decision-making?",
        3, [
        Paragraph("<b>Opportunity cost = value of the next-best alternative foregone.</b> In investment terms it is "
                  "the return on the most profitable opportunity that was rejected, compared to the return on the option "
                  "actually chosen.", A_BODY),
        Paragraph("<b>Importance:</b>", A_BODY),
        *b([
            "Resources are scarce — capital should flow to its highest-value use.",
            "Forces honest comparison of alternatives rather than evaluating a choice in isolation.",
            "Underpins every consumer, investment, business and policy decision (e.g. the 2010 ten-thousand-bitcoin pizza, valued at ~US$41 then and over US$690m by 2024).",
        ]),
    ]))

    s.append(qa("1.4",
        "Explain the concept of market price and the factors that influence its determination.",
        3, [
        Paragraph("<b>Market price</b> is the price at which <b>quantity supplied = quantity demanded</b> "
                  "(market equilibrium). It is set by the interaction of supply and demand, not by any single party.",
                  A_BODY),
        Paragraph("<b>Factors that influence it:</b>", A_BODY),
        *b([
            "<b>Demand side:</b> consumer income, tastes, expectations, prices of substitutes &amp; complements, population.",
            "<b>Supply side:</b> input costs, technology, taxes / subsidies, number of producers, expectations.",
            "<b>External:</b> regulation, exchange rates, weather (commodities), political risk.",
        ]),
    ]))

    s.append(qa("1.5",
        "What is the difference between opportunity cost and risk in economics?", 3, [
        small_table(
            ["", "<b>Opportunity cost</b>", "<b>Risk</b>"],
            [["What it measures",
              "Value of the alternative <b>given up</b>",
              "Possibility that actual return differs from expected; potential loss of capital"],
             ["When it bites",
              "At the moment of choice — comparing options",
              "After the choice is made — uncertainty within the chosen option"],
             ["Certainty",
              "Knowable relative to the decision",
              "Probabilistic / unknown ex-ante"]],
            col_widths=[34 * mm, None, None]
        ),
    ]))

    # ===================== Q2 [9] =====================
    s.append(section_title("QUESTION 2 · Macro vs Micro [9 marks]"))

    s.append(qa("2.1",
        "What is the primary focus of macroeconomics, and how does it differ from microeconomics?",
        3, [
        Paragraph("<b>Macroeconomics</b> studies the economy as a whole — aggregates such as GDP, inflation, "
                  "unemployment, interest rates, exchange rates and government budgets. It evaluates "
                  "<b>monetary &amp; fiscal policy</b> and the business cycle.", A_BODY),
        Paragraph("<b>Microeconomics</b> studies <b>individual</b> agents — households, firms and specific markets — "
                  "and how they make choices over scarce resources (supply, demand, prices, elasticity, market structures).",
                  A_BODY),
        Paragraph("Macro = the forest (whole economy); Micro = the trees (individual actors).", A_BODY),
    ]))

    s.append(qa("2.2",
        "Why are macroeconomic factors significant for investors, and how do they impact investment portfolios?",
        3, [
        Paragraph("Macro factors set the <b>backdrop</b> against which all asset prices move:", A_BODY),
        *b([
            "<b>GDP growth</b> drives corporate earnings → equity returns.",
            "<b>Interest rates &amp; inflation</b> drive bond yields and the discount rate used to value all assets.",
            "<b>Currency moves</b> translate offshore earnings and rebase imported costs.",
            "<b>Policy stance</b> (fiscal expansion / contraction) alters risk premia and sector rotation.",
        ]),
        Paragraph("Portfolio impact shows up in <b>asset allocation</b> (equity vs bonds vs cash), <b>duration</b>, "
                  "<b>sector tilts</b>, and <b>geographic / currency exposure</b>.", A_BODY),
    ]))

    s.append(qa("2.3",
        "What are the key principles studied in microeconomics, and how do they relate to human decision-making?",
        3, [
        *b([
            "<b>Rational choice &amp; utility maximisation</b> — agents pick the option giving the most satisfaction within their budget.",
            "<b>Marginal analysis</b> — decisions are made at the margin (one extra unit), not on totals.",
            "<b>Law of supply &amp; demand</b> — prices coordinate buyers and sellers; surpluses and shortages self-correct.",
            "<b>Elasticity</b> — how strongly demand or supply responds to price changes; informs pricing &amp; taxation.",
            "<b>Market structures</b> (perfect competition, monopolistic, oligopoly, monopoly) — shape pricing power and consumer welfare.",
        ]),
        Paragraph("These principles model the trade-offs households and firms face every day: buy or save, work or leisure, "
                  "produce locally or import, invest in project A or project B.", A_BODY),
    ]))

    # ===================== Q3 [9] =====================
    s.append(section_title("QUESTION 3 · Positive vs Normative [9 marks]"))

    s.append(qa("3.1",
        "What is the difference between positive economics and normative economics?", 3, [
        small_table(
            ["", "<b>Positive</b>", "<b>Normative</b>"],
            [["Question asked", "What <b>is</b>?", "What <b>should be</b>?"],
             ["Nature", "Descriptive, fact-based, testable", "Prescriptive, value-laden, opinion-based"],
             ["Example", "“CPI inflation in SA is 5.2%”", "“Inflation is too high — SARB must hike”"]],
            col_widths=[34 * mm, None, None]
        ),
    ]))

    s.append(qa("3.2", "What are the key characteristics of positive economics?", 3, [
        *b([
            "<b>Objective</b> — independent of personal preferences or value judgements.",
            "<b>Empirical</b> — claims are testable against data and can be falsified.",
            "<b>Model-driven</b> — uses theory (e.g. supply &amp; demand) to derive cause-and-effect relationships.",
            "<b>Predictive</b> — generates if-then statements that can be checked in the real world.",
        ]),
    ]))

    s.append(qa("3.3", "How does normative economics relate to behavioural economics?", 3, [
        Paragraph("<b>Normative</b> economics prescribes what people <i>ought</i> to do (rational, utility-maximising). "
                  "<b>Behavioural</b> economics studies what people <i>actually</i> do — incorporating cognitive biases, "
                  "heuristics and emotion.", A_BODY),
        *b([
            "Behavioural findings (loss aversion, anchoring, herding, framing) reveal where real behaviour <b>departs</b> from the rational ideal.",
            "This challenges classical normative prescriptions and informs <b>policy &amp; product design</b> — nudges, default opt-ins, simplified disclosures.",
            "Together they shape modern welfare economics: design systems that improve outcomes given how humans actually decide.",
        ]),
    ]))

    # ===================== Q4 [24] =====================
    s.append(section_title("QUESTION 4 · Demand &amp; Supply [24 marks]"))

    s.append(qa("4.1", "Explain consumer choice theory and its relationship to demand theory.", 4, [
        Paragraph("<b>Consumer choice theory</b> says consumers seek to maximise their <b>utility</b> "
                  "(satisfaction) subject to a budget constraint. They allocate spending so the <b>marginal "
                  "utility per rand</b> is equal across all goods.", A_BODY),
        *b([
            "<b>Diminishing marginal utility:</b> each extra unit of a good adds less satisfaction than the one before.",
            "So consumers are only willing to buy more if the <b>price falls</b>.",
            "This produces a <b>downward-sloping demand curve</b> — the foundation of demand theory.",
            "Consumer choice → individual demand → market demand.",
        ]),
    ]))

    s.append(qa("4.2", "What is the difference between a change in demand and a change in quantity demanded?",
                4, [
        small_table(
            ["", "Change in <b>quantity demanded</b>", "Change in <b>demand</b>"],
            [["Cause", "Price of the good itself", "Any non-price factor"],
             ["Effect on curve", "<b>Movement ALONG</b> the curve", "<b>SHIFT</b> of the whole curve"],
             ["Examples", "Petrol price rises → fewer litres bought", "Income rises → demand for cars shifts right"]],
            col_widths=[28 * mm, None, None]
        ),
        Spacer(1, 4),
        Paragraph("Distinguishing the two is essential for correctly identifying new equilibria after a shock.",
                  A_BODY),
    ]))

    s.append(qa("4.3", "How does the demand curve typically behave, and what does it represent?", 4, [
        *b([
            "Slopes <b>downward</b> left-to-right — an <b>inverse relationship</b> between price and quantity demanded.",
            "Shows the maximum quantity consumers are willing &amp; able to buy at each price, holding all else constant (ceteris paribus).",
            "Price is plotted on the <b>Y-axis</b> as the independent variable — an exception to standard maths convention.",
            "Underlying causes: diminishing marginal utility, the substitution effect (switch to cheaper alternatives) and the income effect.",
        ]),
    ]))

    s.append(qa("4.4", "What factors can cause a shift in the demand curve?", 4, [
        *b([
            "<b>Income</b> — rises in disposable income increase demand for normal goods, decrease it for inferior goods.",
            "<b>Tastes &amp; preferences</b> — fashion, health trends, advertising.",
            "<b>Prices of related goods</b> — substitutes (rival products) and complements (paired products).",
            "<b>Expectations</b> — anticipated price changes or income shocks pull purchases forward or push them back.",
            "<b>Number of buyers</b> — population growth, demographic shifts, new market access.",
            "<b>Government policy</b> — taxes, subsidies, regulation that change effective price.",
        ]),
    ]))

    s.append(qa("4.5", "What is demand elasticity, and how does it impact businesses?", 4, [
        Paragraph("<b>Price elasticity of demand (PED)</b> = % change in quantity demanded ÷ % change in price.",
                  A_BODY),
        *b([
            "<b>PED &gt; 1 — elastic:</b> quantity highly responsive; price cuts <i>raise</i> revenue.",
            "<b>PED &lt; 1 — inelastic:</b> quantity barely changes; price hikes <i>raise</i> revenue (e.g. fuel, basic foods).",
            "<b>PED = 1 — unit elastic:</b> revenue unchanged.",
        ]),
        Paragraph("<b>Business impact:</b> guides pricing strategy, tax incidence forecasting, promotional design, "
                  "and resilience modelling — necessities can absorb price pressure; luxuries cannot.", A_BODY),
    ]))

    s.append(qa("4.6", "Describe the law of supply and how it is represented by the supply curve.", 4, [
        Paragraph("<b>Law of supply:</b> all else equal, the quantity producers are willing to supply <b>rises</b> "
                  "as the price rises, and falls as the price falls.", A_BODY),
        *b([
            "Driven by <b>profit incentive</b> (higher price → higher margin) and <b>increasing marginal cost</b> (extra units cost more to produce).",
            "Represented by an <b>upward-sloping</b> supply curve.",
            "<b>Movement along</b> the curve = price-only change; <b>shift</b> of the curve = costs, technology, taxes, number of producers, expectations.",
            "Together with the demand curve, the supply curve fixes the <b>market equilibrium</b> price and quantity.",
        ]),
    ]))

    # ===================== Q5 [12] =====================
    s.append(section_title("QUESTION 5 · Fiscal Policy [12 marks]"))

    s.append(qa("5.1", "Discuss the advantages of fiscal policy.", 6, [
        *b([
            "<b>Direct &amp; powerful</b> impact on aggregate demand via government spending and tax changes — particularly effective at the <b>zero lower bound</b> where monetary policy is exhausted.",
            "<b>Targeted</b> — can be channelled at specific sectors, regions or groups (infrastructure, health, social grants) rather than across the whole economy.",
            "<b>Automatic stabilisers</b> (UIF, progressive tax, unemployment grants) smooth shocks without new legislation.",
            "<b>Long-run capacity</b> — productive investment in infrastructure, education and R&amp;D raises potential GDP, not just current demand.",
            "<b>Distributional</b> — can address inequality and poverty directly through tax-and-transfer choices.",
            "<b>Democratically accountable</b> — every line item passes through Parliament's budget process, giving transparency.",
        ]),
    ]))

    s.append(qa("5.2", "Discuss the disadvantages of fiscal policy.", 6, [
        *b([
            "<b>Political delays</b> — budget cycles are long; legislation can take months, by which time the shock has passed.",
            "<b>Debt accumulation</b> — persistent deficits raise the debt-to-GDP ratio and threaten fiscal sustainability.",
            "<b>Crowding-out</b> — heavy government borrowing pushes up bond yields, raising the cost of capital for private investment.",
            "<b>Implementation lags</b> — even once approved, infrastructure spend can take years to land in the real economy.",
            "<b>Risk of inefficiency &amp; political capture</b> — spending may chase votes rather than economic return.",
            "<b>Sovereign / currency consequences</b> — credit-rating downgrades, capital flight and currency weakness if markets lose confidence in the fiscal path.",
        ]),
    ]))

    # ===================== Q6 [15] =====================
    s.append(section_title("QUESTION 6 · The Business Cycle [15 marks]"))

    s.append(qa("6.1",
        "Identify the phase of economic activity being experienced at each point on the business cycle "
        "graph and complete the table.", 4, [
        small_table(
            ["Position", "Phase of Economic Activity"],
            [["Point A", "<b>Trough</b> — lowest point of the cycle; output below long-term trend; high unemployment."],
             ["Points A to B", "<b>Expansion / Recovery</b> — output rising back towards and above potential."],
             ["Point B", "<b>Peak</b> — cycle high; economy at or above potential; capacity constraints &amp; inflation pressure."],
             ["Points B to C", "<b>Contraction / Recession</b> — output falling; rising unemployment; falling demand."]],
            col_widths=[34 * mm, None]
        ),
    ]))

    s.append(qa("6.2",
        "Complete the table below with the most likely direction of economic indicators during the "
        "identified phases.", 3, [
        small_table(
            ["Indicator", "Points A → B (Expansion)", "Points B → C (Contraction)"],
            [["Gross Domestic Product",
              "<b>↑ Rising</b> — output expanding above trend",
              "<b>↓ Falling</b> — output contracting"],
             ["Unemployment",
              "<b>↓ Falling</b> — hiring picks up as demand grows",
              "<b>↑ Rising</b> — retrenchments, lower vacancies"],
             ["Consumer Price Index",
              "<b>↑ Rising</b> — demand pulls prices up, often peaking late in expansion",
              "<b>↓ Falling / moderating</b> — slack demand cools prices; risk of deflation in deep recessions"]],
            col_widths=[40 * mm, None, None]
        ),
    ]))

    s.append(qa("6.3",
        "If South Africa's economic activity was at a point moving from B to C on the above graph, "
        "how would you expect investments in equities and bonds to be performing?", 8, [
        Paragraph("Movement from <b>B to C is a contraction / recession</b> — output falling, unemployment rising, "
                  "inflation moderating, central bank typically <b>cutting</b> rates to support growth.", A_BODY),
        Paragraph("<b>Equity markets — poor performance overall:</b>", A_BODY),
        *b([
            "Corporate <b>earnings fall</b> as demand and pricing power weaken → equity prices decline.",
            "<b>Risk premium widens</b> → multiples compress; investors rotate <b>out of cyclicals</b> (banks, industrials, discretionary) <b>into defensives</b> (consumer staples, healthcare, utilities, gold).",
            "Dividends may be cut; smaller caps and highly geared companies hit hardest.",
        ]),
        Paragraph("<b>Bond markets — typically strong performance:</b>", A_BODY),
        *b([
            "Falling rates &amp; rate-cut expectations push <b>bond yields down</b> → bond <b>prices up</b> (inverse relationship).",
            "<b>Flight to safety</b> drives flows into government bonds, supporting long-duration sovereigns most.",
            "<b>Credit spreads widen</b>, so investment-grade tends to outperform high-yield / junk; weak credits face higher default risk.",
            "Net: a contraction is generally <b>bad for equities, good for high-grade duration</b> — the textbook case for a defensive equity / long-bond rotation late in the cycle.",
        ]),
    ]))

    # ===================== Q7 [8] =====================
    s.append(section_title("QUESTION 7 · CPI Calculation [8 marks]"))

    s.append(qa("7.1", "Calculate the cost of this basket in 2023 and 2024. Show your calculations.", 4, [
        small_table(
            ["Good", "Qty", "2023 Price", "2023 Cost", "2024 Price", "2024 Cost"],
            [["Chickens",  "48",  "12.50", "<b>600.00</b>",  "12.90", "<b>619.20</b>"],
             ["Bread",    "120",  "1.15",  "<b>138.00</b>",  "1.25",  "<b>150.00</b>"],
             ["Soccer Tickets", "18", "45.00", "<b>810.00</b>", "46.00", "<b>828.00</b>"],
             ["<b>BASKET TOTAL</b>", "", "", "<b>1 548.00</b>", "", "<b>1 597.20</b>"]],
            col_widths=[32 * mm, 14 * mm, 22 * mm, 26 * mm, 22 * mm, 26 * mm]
        ),
        Spacer(1, 4),
        Paragraph("<b>2023 basket =</b> (48 × 12.50) + (120 × 1.15) + (18 × 45.00) = 600 + 138 + 810 = "
                  "<b>1 548.00</b>", A_BODY),
        Paragraph("<b>2024 basket =</b> (48 × 12.90) + (120 × 1.25) + (18 × 46.00) = 619.20 + 150.00 + 828.00 = "
                  "<b>1 597.20</b>", A_BODY),
    ]))

    s.append(qa("7.2",
        "Using your 7.1 results, calculate a consumer price index with 2023 as the base year. "
        "Show your calculations.", 2, [
        Paragraph("CPI<sub>year</sub> = (Cost of basket in year ÷ Cost of basket in base year) × 100", A_BODY),
        *b([
            "<b>CPI 2023 = (1 548.00 / 1 548.00) × 100 = 100.00</b> (base year)",
            "<b>CPI 2024 = (1 597.20 / 1 548.00) × 100 = 103.18</b>",
        ]),
    ]))

    s.append(qa("7.3", "Calculate the rate of inflation in Country ABC in 2024. Show your calculations.", 2, [
        Paragraph("Inflation rate = (CPI<sub>2024</sub> − CPI<sub>2023</sub>) ÷ CPI<sub>2023</sub> × 100", A_BODY),
        Paragraph("= (103.18 − 100.00) / 100.00 × 100 = <b>3.18%</b>", A_BODY),
    ]))

    # ===================== Q8 [5] =====================
    s.append(section_title("QUESTION 8 · US Retail Sales Extract [5 marks]"))

    s.append(qa("8.1",
        "Based on your knowledge of the business cycle, what stage of the economic cycle "
        "does this country appear to be in?", 1, [
        Paragraph("<b>Expansion — likely late expansion / approaching the peak.</b> The 6.2% annual jump in "
                  "retail sales is the strongest in four years, with durables rising 1.7% in a single month — "
                  "consistent with strong consumer demand and a maturing upswing.", A_BODY),
    ]))

    s.append(qa("8.2", "How would you expect the equity markets to have performed during "
                "the calendar year referenced?", 2, [
        Paragraph("Equity markets would likely have <b>performed strongly</b>:", A_BODY),
        *b([
            "Strong consumer spending → strong corporate earnings, especially in consumer discretionary &amp; durables.",
            "Rising risk appetite &amp; confidence support multiple expansion alongside earnings growth.",
        ]),
    ]))

    s.append(qa("8.3", "Explain why bond prices would fall on the back of stronger than "
                "expected retail sales.", 2, [
        *b([
            "Strong sales raise <b>inflation expectations</b> and the likelihood that the central bank will <b>hike interest rates</b>.",
            "Higher expected policy rates push <b>bond yields up</b>, and because bond <b>yields and prices move inversely</b>, bond <b>prices fall</b>.",
        ]),
    ]))

    # ===================== Q9 [13] =====================
    s.append(section_title("QUESTION 9 · Monetary Policy &amp; SARB [13 marks]"))

    s.append(qa("9.1", "What is the repo rate and how does the lowering of this rate affect the local economy?",
                4, [
        Paragraph("The <b>repo rate</b> (repurchase rate) is the rate at which the <b>South African Reserve Bank "
                  "lends short-term funds to commercial banks</b> against eligible collateral. It is the SARB's "
                  "headline monetary policy lever.", A_BODY),
        Paragraph("<b>Effect of a cut:</b>", A_BODY),
        *b([
            "Banks' wholesale funding becomes cheaper → they pass on lower lending rates (prime, mortgages, business credit).",
            "Cheaper credit stimulates <b>household consumption</b> and <b>business investment</b> → boosts aggregate demand and employment.",
            "Bond yields fall → bond prices rise; equity markets often rally on cheaper discount rates.",
            "Rand may <b>weaken</b> on narrower yield differentials, supporting exporters but lifting imported-inflation risk.",
        ]),
    ]))

    s.append(qa("9.2",
        "What other tools are available to a central bank wishing to implement expansionary monetary policy? "
        "Your answer should demonstrate your understanding of how each tool operates, its effects on market "
        "participants and how it works to encourage economic growth.", 4, [
        *b([
            "<b>Open Market Operations (OMO)</b> — SARB <b>buys</b> government bonds in the market, paying with newly created reserves. Bank liquidity rises, short-term rates fall, banks lend more freely → credit, spending and investment expand.",
            "<b>Reserve requirement cuts</b> — lowering the minimum % of deposits banks must hold at the central bank frees up cash for lending. Each rand of reserves supports more credit through the money multiplier.",
            "<b>Quantitative Easing (QE)</b> — large-scale purchases of long-dated government and sometimes corporate bonds beyond normal OMOs. Pushes <b>long-end yields</b> down, raises asset prices, encourages risk-taking and investment; deployed when the policy rate is at or near the zero lower bound.",
            "<b>Forward guidance</b> — explicit communication that rates will stay low (or be cut further). Anchors market expectations of future short rates, pulling longer-term yields down today and encouraging investment.",
        ]),
    ]))

    s.append(qa("9.3", "Describe the SARB's mandate in terms of inflation management.", 5, [
        *b([
            "<b>Constitutional mandate (s224):</b> protect the value of the currency in the interest of <b>balanced and sustainable economic growth</b>.",
            "Operates a <b>flexible inflation-targeting</b> framework with a target band of <b>3% to 6%</b> for headline CPI (with a 4.5% midpoint preferred).",
            "The <b>Monetary Policy Committee (MPC)</b> sets the repo rate to bring inflation back toward target over the policy horizon, while considering output and employment effects.",
            "<b>Operationally independent</b> from the executive — protected by legislation to ensure credibility and anchor inflation expectations.",
            "Reinforced by <b>transparency</b>: published MPC statements, Monetary Policy Reviews and inflation forecasts; uses the full monetary toolkit (repo, OMO, reserves, forward guidance) to support price stability.",
        ]),
    ]))

    # Totals footer
    s.append(Spacer(1, 8))
    s.append(Paragraph(
        "<b>Total marks: 110</b> &nbsp;|&nbsp; Q1: 15 · Q2: 9 · Q3: 9 · Q4: 24 · Q5: 12 · Q6: 15 · Q7: 8 · Q8: 5 · Q9: 13",
        ParagraphStyle("totals", fontName="Helvetica", fontSize=9, textColor=MUTED, leading=12, alignment=1)
    ))

    doc.build(s)
    print("Wrote:", OUTPUT)


if __name__ == "__main__":
    build()
