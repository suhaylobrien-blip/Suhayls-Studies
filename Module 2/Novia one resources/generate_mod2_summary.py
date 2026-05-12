"""Generate condensed Module 2 study summary PDF — Module 1 style, with proper breathing room."""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    KeepTogether, FrameBreak, Image,
)

DIAG_DIR = r"C:\Users\SuhaylO'Brien\OneDrive - BrickField Canvas\Documents\NOVIA ONE\Module 2\diagrams"

OUTPUT = r"C:\Users\SuhaylO'Brien\OneDrive - BrickField Canvas\Documents\NOVIA ONE\Module 2\FMP Module 2 - Condensed Study Summary.pdf"

NAVY      = colors.HexColor("#121338")
ORANGE    = colors.HexColor("#D4471A")
GREY_BG   = colors.HexColor("#F2F2F2")
RULE      = colors.HexColor("#CCCCCC")
TEXT      = colors.HexColor("#1A1A1A")
MUTED     = colors.HexColor("#555555")
CALLOUT_BG = colors.HexColor("#FFF3E6")
TABLE_HEAD = NAVY

PAGE_W, PAGE_H = A4
HEADER_H  = 12 * mm
FOOTER_H  = 10 * mm
M_TOP     = HEADER_H + 6 * mm
M_BOTTOM  = FOOTER_H + 4 * mm
M_LEFT    = 12 * mm
M_RIGHT   = 12 * mm
GUTTER    = 7 * mm

PAGE_TITLE = "FMP MODULE 2 — FUNDAMENTALS OF ECONOMICS"
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


# --- Styles (more generous leading, balanced fonts) ---
H1 = ParagraphStyle(
    "H1", fontName="Helvetica-Bold", fontSize=10.5, textColor=colors.white,
    leading=13, backColor=NAVY, borderPadding=(4, 8, 4, 8),
    spaceBefore=6, spaceAfter=6,
)
H2 = ParagraphStyle(
    "H2", fontName="Helvetica-Bold", fontSize=9.2, textColor=NAVY,
    leading=12, spaceBefore=5, spaceAfter=3,
)
BODY = ParagraphStyle(
    "B", fontName="Helvetica", fontSize=8.6, textColor=TEXT, leading=11.5,
    spaceAfter=3.5,
)
BODY_B = ParagraphStyle(
    "BB", fontName="Helvetica-Bold", fontSize=8.6, textColor=TEXT, leading=11.5,
    spaceAfter=3.5,
)
BULLET = ParagraphStyle(
    "BU", fontName="Helvetica", fontSize=8.6, textColor=TEXT, leading=11.5,
    leftIndent=11, bulletIndent=2, spaceAfter=2.5,
)
CALL_TITLE = ParagraphStyle(
    "CT", fontName="Helvetica-Bold", fontSize=8.5, textColor=ORANGE,
    leading=11.5, spaceAfter=3,
)
CALL_BODY = ParagraphStyle(
    "CB", fontName="Helvetica", fontSize=8.6, textColor=TEXT, leading=11.5,
    spaceAfter=2,
)
# Style optimised for use INSIDE table cells — tighter spaceAfter
CELL = ParagraphStyle(
    "CELL", fontName="Helvetica", fontSize=8.4, textColor=TEXT, leading=11,
    spaceAfter=0,
)
CELL_B = ParagraphStyle(
    "CELLB", fontName="Helvetica-Bold", fontSize=8.4, textColor=colors.white,
    leading=11, spaceAfter=0,
)
CELL_HEAD = ParagraphStyle(
    "CH", fontName="Helvetica-Bold", fontSize=8.4, textColor=TEXT, leading=11,
    spaceAfter=0,
)
CAP = ParagraphStyle(
    "cap", fontName="Helvetica-Oblique", fontSize=7.8, textColor=MUTED,
    leading=10, alignment=1, spaceAfter=6,
)


def diagram(name, width):
    import os
    from PIL import Image as PILImage
    path = os.path.join(DIAG_DIR, name)
    im = PILImage.open(path)
    aspect = im.height / im.width
    return Image(path, width=width, height=width * aspect)


def caption(t):
    return Paragraph(t, CAP)


def hsection(text):
    return Paragraph(text, H1)


def sub(text):
    return Paragraph(text, H2)


def p(text):
    return Paragraph(text, BODY)


def pb(text):
    return Paragraph(text, BODY_B)


def bul(items):
    return [Paragraph(f"<font color='#D4471A'>»</font> {it}", BULLET) for it in items]


def callout(title, body_lines):
    rows = [[Paragraph(title, CALL_TITLE)]]
    for line in body_lines:
        rows.append([Paragraph(line, CALL_BODY)])
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
    """Properly-padded table. Cell content is wrapped in Paragraphs so it word-wraps."""
    header_row = [Paragraph(f"<b>{h}</b>", CELL_B) for h in headers]
    body_rows = []
    for r in rows:
        body_rows.append([Paragraph(c, CELL) for c in r])
    data = [header_row] + body_rows
    t = Table(data, colWidths=col_widths, repeatRows=0)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEAD),
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
        title="FMP Module 2 — Condensed Study Summary",
        author="Suhayl O'Brien",
    )

    frame_w = (PAGE_W - M_LEFT - M_RIGHT - GUTTER) / 2
    frame_h = PAGE_H - M_TOP - M_BOTTOM
    L = Frame(M_LEFT, M_BOTTOM, frame_w, frame_h, showBoundary=0,
              leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    R = Frame(M_LEFT + frame_w + GUTTER, M_BOTTOM, frame_w, frame_h, showBoundary=0,
              leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="two_col", frames=[L, R],
                                       onPage=header_footer)])

    s = []
    fw = frame_w

    # =================== PAGE 1 — LEFT ===================
    s.append(hsection("CHAPTER 1.1 · INTRODUCTION TO ECONOMICS"))
    s.append(p("<b>Economics:</b> the study of choice under <b>scarcity</b> — unlimited wants meet limited resources. Three core questions: <b>What</b> to produce? <b>How</b> to produce it? <b>For whom</b>?"))
    s.append(p("<b>Scarcity</b> can also describe a market move — a fall in supply relative to demand pushing a new equilibrium price."))

    s.append(sub("1.1.2 Opportunity Cost"))
    s.append(p("Value of the next-best alternative foregone when a choice is made."))
    s.extend(bul([
        "<b>Explicit costs:</b> actual cash outflows — measurable, recorded in accounts.",
        "<b>Implicit costs:</b> no cash changes hands but real value is foregone (e.g. owner's unpaid time).",
        "<b>Risk vs Opportunity Cost:</b> risk is loss of capital; opportunity cost is the return given up by choosing one investment over another.",
    ]))
    s.append(callout("CASE STUDY · The Most Expensive Pizza",
                     ["In 2010, 10,000 BTC bought two pizzas (worth ~$41 then). By Aug 2024 the holding was worth over <b>US$690 million</b> — the textbook illustration of opportunity cost."]))

    s.append(sub("1.1.3 Market Price"))
    s.append(p("The price at which <b>quantity supplied = quantity demanded</b>. Determined by the interaction of supply &amp; demand."))
    s.extend(bul([
        "<b>Consumer surplus:</b> max price a consumer would pay minus the market price actually paid.",
        "<b>Producer surplus:</b> market price minus the producer's minimum acceptable price (cost).",
    ]))

    # ========== PAGE 1 — RIGHT ==========
    s.append(FrameBreak())

    s.append(sub("1.1.5 / 1.1.6 Macro vs Micro"))
    s.append(tbl(
        ["Macroeconomics", "Microeconomics"],
        [["Whole economy — GDP, inflation, unemployment, exchange rates, monetary &amp; fiscal policy.",
          "Individual firms, households &amp; markets — supply, demand, prices, consumer &amp; producer behaviour."]],
        col_widths=[fw * 0.5, fw * 0.5]
    ))

    s.append(sub("1.1.8–1.1.9 Theory: Assumptions &amp; Schools"))
    s.append(p("Economists build models on <b>simplifying assumptions</b> — rational agents, perfect info, ceteris paribus, profit / utility maximisation."))
    s.append(p("<b>Neo-classical</b> view: rational behaviour, free markets and competition drive efficient outcomes."))
    s.append(tbl(
        ["Positive Economics", "Normative Economics"],
        [["Objective, fact-based — describes <b>what IS</b>; testable against evidence.",
          "Subjective, value-based — prescribes <b>what SHOULD BE</b>; opinion-driven."]],
        col_widths=[fw * 0.5, fw * 0.5]
    ))

    s.append(hsection("1.2 THEORY OF DEMAND &amp; SUPPLY"))

    s.append(sub("1.2.2 Supply Curve"))
    s.append(p("Slopes <b>upward</b>: higher price → suppliers willing to supply more. The <b>independent variable (price) is plotted on the Y-axis</b> — exception to maths convention."))

    s.append(sub("1.2.3 Demand Curve"))
    s.append(p("Slopes <b>downward</b> (inverse): higher price → less demanded. Same Y-axis price convention."))

    # =================== PAGE 2 — LEFT ===================
    s.append(FrameBreak())

    s.append(sub("1.2.4 Movement vs Shift"))
    s.extend(bul([
        "<b>Change in quantity demanded / supplied</b> = <b>movement ALONG</b> the curve, caused by price ONLY.",
        "<b>Change in demand / supply</b> = <b>SHIFT</b> of the whole curve, caused by income, tastes, expectations, prices of related goods, input costs, technology, taxes / subsidies.",
    ]))

    s.append(sub("1.2.5 Market Equilibrium"))
    s.append(p("Where supply &amp; demand curves intersect — <b>Qs = Qd</b> at the equilibrium price."))
    s.extend(bul([
        "<b>Price &gt; equilibrium → surplus</b> (excess supply).",
        "<b>Price &lt; equilibrium → shortage</b> (excess demand).",
    ]))
    s.append(diagram("supply_demand.png", fw))
    s.append(caption("Demand slopes down, supply slopes up — equilibrium where they cross."))

    s.append(sub("Price Elasticity (PED / PES)"))
    s.append(p("% change in quantity for a 1% change in price."))
    s.append(tbl(
        ["Value", "Interpretation"],
        [["&gt; 1",  "Elastic — quantity highly responsive."],
         ["&lt; 1", "Inelastic — quantity barely changes (necessities, fuel)."],
         ["= 1",    "Unit elastic."],
         ["= 0",    "Perfectly inelastic — vertical curve."],
         ["= ∞",    "Perfectly elastic — horizontal curve."]],
        col_widths=[fw * 0.22, fw * 0.78]
    ))

    s.append(sub("1.2.7 Price Ceiling vs Price Floor"))
    s.append(tbl(
        ["Tool", "Effect"],
        [["<b>Price ceiling</b><br/>max — set BELOW equilibrium",
          "Shortage; rationing, black markets, lower investment. e.g. rent control."],
         ["<b>Price floor</b><br/>min — set ABOVE equilibrium",
          "Surplus; unsold inventory or unemployment. e.g. minimum wage, ag price support."]],
        col_widths=[fw * 0.40, fw * 0.60]
    ))

    s.append(callout("MEMORISE · The 3 Rules of Curves",
                     ["1. Price on Y-axis (exception to maths convention).",
                      "2. Movement along curve = price-only change.",
                      "3. Shift of curve = any other factor changes."]))

    s.append(diagram("price_controls.png", fw))
    s.append(caption("Ceiling pinned BELOW equilibrium → shortage. Floor pinned ABOVE → surplus."))

    # =================== PAGE 2 — RIGHT ===================
    s.append(FrameBreak())

    s.append(hsection("1.3 MARKET STRUCTURES"))
    s.append(p("Defined by <b>number of firms, product differentiation, barriers to entry, pricing power</b> and access to information."))
    s.append(tbl(
        ["Structure", "Key Features"],
        [["<b>Perfect Competition</b>",
          "Many small firms, identical products, price takers, free entry / exit, perfect info. Zero economic profit long-run."],
         ["<b>Monopolistic<br/>Competition</b>",
          "Many firms, differentiated products, some pricing power, low entry barriers (e.g. restaurants, retail)."],
         ["<b>Oligopoly</b>",
          "Few large firms, identical or differentiated products, high barriers, strategic interdependence, may collude."],
         ["<b>Monopoly</b>",
          "Single firm, no close substitutes, price maker, very high barriers, regulated where it persists."]],
        col_widths=[fw * 0.32, fw * 0.68]
    ))

    s.append(hsection("1.4 BEHAVIOURAL ECONOMICS"))
    s.append(p("Combines economics with psychology — real people deviate from the rational-agent ideal due to <b>heuristics, biases, emotions</b> and social context."))

    # =================== PAGE 3 — LEFT ===================
    s.append(FrameBreak())

    s.append(sub("Traditional vs Behavioural Finance"))
    s.append(tbl(
        ["Traditional", "Behavioural"],
        [["Rational utility maximisers, perfect info, mean-variance optimisation (Markowitz, CAPM), efficient markets.",
          "Bounded rationality; biases (overconfidence, anchoring, herding, loss aversion, mental accounting, framing). Explains bubbles &amp; momentum."]],
        col_widths=[fw * 0.5, fw * 0.5]
    ))

    s.append(sub("1.4.6 Utility Theory"))
    s.append(p("Consumers maximise <b>utility</b> (satisfaction) given prices and budget; subject to <b>diminishing marginal utility</b> — each extra unit adds less satisfaction."))

    s.append(sub("1.4.7 Efficient Market Hypothesis (EMH)"))
    s.append(tbl(
        ["Form", "Information Reflected"],
        [["<b>Weak</b>",
          "All historical price &amp; volume data → technical analysis cannot consistently beat the market."],
         ["<b>Semi-strong</b>",
          "All public information → fundamental analysis cannot consistently beat the market."],
         ["<b>Strong</b>",
          "All info incl. private / insider → no one can consistently beat the market."]],
        col_widths=[fw * 0.25, fw * 0.75]
    ))
    s.append(p("<b>Criticisms:</b> persistent anomalies, asset bubbles and behavioural patterns all challenge especially the strong form."))

    s.append(hsection("1.5 MACRO ECONOMICS"))
    s.append(p("Whole-economy lens: inflation, unemployment, growth, exchange rates, balance of payments, fiscal &amp; monetary policy."))

    s.append(sub("1.5.1 Schools of Macro Thought"))
    s.extend(bul([
        "<b>Classical:</b> markets self-correct, prices &amp; wages flexible.",
        "<b>Keynesian:</b> demand drives output; active fiscal policy in recessions.",
        "<b>Monetarist:</b> money supply growth is the key driver of inflation (Friedman).",
        "<b>Neo-classical &amp; Neo-Keynesian:</b> blend rational expectations with short-run rigidities.",
        "<b>Supply-side:</b> tax cuts &amp; deregulation to expand productive capacity.",
    ]))
    s.append(p("<b>Limitations of macro:</b> many variables, simplifying assumptions, long &amp; variable time-lags, political interference."))

    # =================== PAGE 3 — RIGHT ===================
    s.append(FrameBreak())

    s.append(sub("1.5.2 Economic Growth — Preconditions"))
    s.extend(bul([
        "Human capital (skills, education)",
        "Physical capital &amp; infrastructure",
        "Technology &amp; productivity (TFP)",
        "Natural resources",
        "Stable institutions, rule of law, policy certainty",
    ]))

    s.append(sub("1.5.3 Components of GDP (Expenditure)"))
    s.append(callout("FORMULA · MEMORISE",
                     ["<b>GDP (Y) = C + I + G + (X − M)</b>",
                      "C = household Consumption · I = business Investment · G = Government spending · X−M = net exports."]))
    s.append(diagram("gdp_components.png", fw))
    s.append(caption("Household consumption dominates SA GDP; net exports are small but variable."))
    s.append(p("<b>Income approach:</b> GDP = wages + rents + interest + profits."))
    s.append(p("<b>Y = C + S</b> — Income equals Consumption + Savings."))
    s.append(p("<b>MPC</b> (Marginal Propensity to Consume) = fraction of each extra rand of income spent."))

    s.append(sub("1.5.4 Nominal vs Real GDP"))
    s.append(tbl(
        ["Measure", "Definition"],
        [["<b>Nominal GDP</b>",
          "Output at <b>current</b> prices — includes inflation."],
         ["<b>Real GDP</b>",
          "Output at <b>constant base-year</b> prices — true measure of volume."],
         ["<b>GDP Deflator</b>",
          "Nominal / Real × 100 → economy-wide price level."]],
        col_widths=[fw * 0.30, fw * 0.70]
    ))

    s.append(sub("1.5.5 Growth Rate Formula"))
    s.append(callout("FORMULA",
                     ["<b>Growth = (Y<sub>1</sub> − Y<sub>0</sub>) / Y<sub>0</sub> × 100</b>",
                      "Real growth uses real GDP — strips out inflation."]))

    # =================== PAGE 4 — LEFT ===================
    s.append(FrameBreak())

    s.append(hsection("1.6 THE BUSINESS CYCLE"))
    s.append(p("Repetitive fluctuations in real GDP around its long-run potential path."))
    s.append(diagram("business_cycle.png", fw))
    s.append(caption("Four phases: trough → expansion → peak → contraction. Long-term trend slopes up."))
    s.extend(bul([
        "<b>Expansion</b> — rising output, falling unemployment.",
        "<b>Peak</b> — economy operating above potential; inflationary pressure builds.",
        "<b>Contraction / recession</b> — falling output (two consecutive quarters of negative GDP growth).",
        "<b>Trough</b> — low point; idle capacity, high unemployment.",
        "<b>Recovery</b> — output picks up back toward potential.",
    ]))
    s.append(p("<b>Output gap</b> = Actual − Potential GDP. Positive → inflationary; negative → deflationary &amp; unemployment."))

    s.append(hsection("1.7 UNEMPLOYMENT"))
    s.append(tbl(
        ["Type", "Cause"],
        [["<b>Frictional</b>",  "Between jobs — voluntary, short-term."],
         ["<b>Structural</b>",  "Skills / location mismatch with available jobs."],
         ["<b>Cyclical</b>",    "Recession-driven downturn in demand for labour."],
         ["<b>Seasonal</b>",    "Predictable seasonal patterns (tourism, agriculture)."]],
        col_widths=[fw * 0.32, fw * 0.68]
    ))
    s.append(p("<b>Natural rate</b> = frictional + structural. Policy generally targets cyclical unemployment."))

    s.append(hsection("1.8 INFLATION"))
    s.append(p("Sustained rise in the general price level — erodes purchasing power, distorts saving &amp; investment, drives wage demands."))

    s.append(sub("1.8.1 Consumer Price Index (CPI)"))
    s.append(callout("FORMULA · CPI",
                     ["<b>CPI = (Cost of basket at current prices / Cost of basket at base-year prices) × 100</b>",
                      "Other measures: PPI (producer prices), GDP deflator (economy-wide)."]))

    # =================== PAGE 4 — RIGHT ===================
    s.append(FrameBreak())

    s.append(sub("1.8.2 Types of Inflation &amp; Effects"))
    s.append(tbl(
        ["Type", "Driver / Impact"],
        [["<b>Demand-pull</b>",
          "Too much demand vs supply — firms can pass costs, equities may benefit short term."],
         ["<b>Cost-push</b>",
          "Input cost rises (oil, wages, FX) — squeezes margins, bad for equities."],
         ["<b>Built-in</b>",
          "Wage-price spiral — entrenched expectations."]],
        col_widths=[fw * 0.32, fw * 0.68]
    ))

    s.append(hsection("1.8.3 MONETARY POLICY"))
    s.append(p("<b>Central bank</b> (SARB) manages money supply &amp; interest rates to anchor inflation and support balanced growth."))

    s.append(sub("Tools"))
    s.extend(bul([
        "<b>Open Market Operations (OMO)</b> — buy / sell government bonds to add / drain liquidity.",
        "<b>Reserve requirements</b> — minimum % of deposits banks must hold.",
        "<b>Repo / discount rate</b> — rate at which SARB lends to commercial banks; the headline policy signal.",
        "<b>Quantitative easing</b> — large-scale asset purchases when rates approach zero.",
        "<b>Forward guidance</b> — communicating the future path of rates to anchor expectations.",
    ]))

    s.append(sub("Stance"))
    s.append(tbl(
        ["Stance", "Effect"],
        [["<b>Expansionary</b>",
          "Lower rates &amp; more liquidity → cheaper credit → spend, invest, grow → inflation."],
         ["<b>Contractionary</b>",
          "Higher rates &amp; less liquidity → cool demand → reduce inflation, slow growth."]],
        col_widths=[fw * 0.32, fw * 0.68]
    ))
    s.append(p("<b>Limits:</b> long &amp; variable lags, liquidity trap at the zero lower bound, blunt against supply-side shocks."))

    # =================== PAGE 5 — LEFT ===================
    s.append(FrameBreak())

    s.append(hsection("1.8.4 FISCAL POLICY"))
    s.append(p("<b>National Treasury</b> uses <b>government spending (G)</b> and <b>taxation (T)</b> to influence aggregate demand."))

    s.append(tbl(
        ["Stance", "Effect"],
        [["<b>Expansionary</b>",
          "↑ G or ↓ T → stimulates demand, growth, employment. Funded by borrowing → deficit."],
         ["<b>Contractionary</b>",
          "↓ G or ↑ T → cools demand, slows growth, reduces deficit."]],
        col_widths=[fw * 0.32, fw * 0.68]
    ))
    s.extend(bul([
        "<b>Budget deficit</b> (G &gt; T) funded by issuing bonds → can lift yields, risk crowding out private investment.",
        "<b>Budget surplus</b> (G &lt; T) reduces public debt, may slow short-run demand.",
        "<b>Discretionary</b> (deliberate policy changes) vs <b>automatic stabilisers</b> (welfare, progressive tax).",
        "<b>Limits:</b> political delays, debt sustainability, crowding-out, time-lags in implementation.",
    ]))

    s.append(callout("EXAM FOCUS · Monetary vs Fiscal",
                     ["<b>Monetary</b>: fast, blunt, controlled by independent central bank — works via rates &amp; credit.",
                      "<b>Fiscal</b>: slower, more targeted, controlled by Treasury / political process — works via spending &amp; tax."]))

    # =================== PAGE 5 — RIGHT ===================
    s.append(FrameBreak())

    s.append(hsection("KEY ACRONYMS &amp; FORMULAS"))
    s.append(tbl(
        ["Term", "Meaning"],
        [["<b>GDP</b>",  "Gross Domestic Product = C + I + G + (X − M)"],
         ["<b>GNP</b>",  "Gross National Product — incl. net income from abroad"],
         ["<b>CPI</b>",  "Consumer Price Index — basket-based inflation measure"],
         ["<b>PPI</b>",  "Producer Price Index — input-side inflation"],
         ["<b>MPC</b>",  "Marginal Propensity to Consume / Monetary Policy Committee"],
         ["<b>TFP</b>",  "Total Factor Productivity"],
         ["<b>PED / PES</b>", "Price Elasticity of Demand / Supply"],
         ["<b>EMH</b>",  "Efficient Market Hypothesis (Weak / Semi / Strong)"],
         ["<b>OMO</b>",  "Open Market Operations (monetary tool)"],
         ["<b>SARB</b>", "South African Reserve Bank — central bank"],
         ["<b>BoP</b>",  "Balance of Payments — current + capital &amp; financial"]],
        col_widths=[fw * 0.25, fw * 0.75]
    ))

    s.append(callout("KEY FORMULAS · ONE-PAGE RECAP",
                     ["GDP (expenditure) = <b>C + I + G + (X − M)</b>",
                      "Y = C + S",
                      "Real GDP = Nominal GDP / GDP Deflator × 100",
                      "Growth rate = (Y<sub>1</sub> − Y<sub>0</sub>) / Y<sub>0</sub> × 100",
                      "CPI = (Cost current basket / Cost base-year basket) × 100",
                      "Inflation rate = (CPI<sub>1</sub> − CPI<sub>0</sub>) / CPI<sub>0</sub> × 100",
                      "PED = % ΔQ<sub>d</sub> / % ΔP"]))

    doc.build(s)
    print("Wrote:", OUTPUT)


if __name__ == "__main__":
    build()
