#!/usr/bin/env python3
"""
Top 10 Winners and Losers in US Listed Exchanges → PDF
- Calculated by daily % change
- Data sourced from Yahoo Finance using yfinance
"""

import yfinance as yf
import pandas as pd
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

# -----------------------------
# 1. Define sample tickers
# -----------------------------
tickers = [
    "AAPL","MSFT","TSLA","GOOG","AMZN","NVDA","FB","NFLX","AMD","INTC",
    "GME","AMC","NIO","SNDL","BB","PLTR","FUBO","RIOT","CLNE","SPCE",
    "F","BBBY","SOS","IQ","CLOV","TRVG","AUPH","EXPR","KOSS"
]

# -----------------------------
# 2. Fetch last 2 days of prices
# -----------------------------
data = []
for ticker in tickers:
    try:
        t = yf.Ticker(ticker)
        hist = t.history(period="2d")
        if len(hist) < 2:
            continue
        prev_close = hist['Close'].iloc[-2]
        last_close = hist['Close'].iloc[-1]
        change = last_close - prev_close
        pct_change = (change / prev_close) * 100
        data.append([ticker, f"${last_close:.2f}", f"{change:+.2f}", f"{pct_change:+.2f}%"])
    except Exception:
        continue

# -----------------------------
# 3. Create DataFrame
# -----------------------------
df = pd.DataFrame(data, columns=["Ticker","Last Price","Change","% Change"])
top_winners = df.sort_values("% Change", ascending=False).head(10)
top_losers  = df.sort_values("% Change").head(10)

# -----------------------------
# 4. Export to PDF
# -----------------------------
def export_pdf(winners, losers, filename="Top_Winners_Losers.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=LETTER,
                            rightMargin=0.75*inch, leftMargin=0.75*inch,
                            topMargin=1*inch, bottomMargin=0.75*inch)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = ParagraphStyle(
        'Title', parent=styles['Title'], fontSize=22, alignment=1,
        textColor=colors.HexColor("#0B3D91"), spaceAfter=20
    )
    now = datetime.now().strftime("%B %d, %Y – %H:%M")
    story.append(Paragraph(f"Top 10 Winners & Losers – {now}", title_style))
    story.append(Spacer(1, 0.2*inch))

    # Helper to add table
    def add_table(df, title, header_bg=colors.HexColor("#006400")):
        story.append(Paragraph(title, styles['Heading2']))
        story.append(Spacer(1, 0.1*inch))
        header = [[Paragraph(f"<b>{c}</b>", styles['Normal']) for c in df.columns]]
        data_table = header + df.values.tolist()
        table = Table(data_table, hAlign='CENTER', colWidths=[1.2*inch,1.2*inch,1.2*inch,1.2*inch])
        style_cmds = [
            ('BACKGROUND', (0,0), (-1,0), header_bg),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ]
        # Alternate row colors
        for i in range(1, len(data_table)):
            bg = colors.HexColor("#f9f9f9") if i % 2 == 1 else colors.white
            style_cmds.append(('BACKGROUND', (0,i), (-1,i), bg))
        table.setStyle(TableStyle(style_cmds))
        story.append(table)
        story.append(Spacer(1, 0.25*inch))

    # Add winners & losers
    add_table(top_winners, "Top 10 Winners", header_bg=colors.HexColor("#228B22"))
    add_table(top_losers, "Top 10 Losers", header_bg=colors.HexColor("#8B0000"))

    # Footer
    footer_style = ParagraphStyle('Footer', parent=styles['Normal'], fontSize=9,
                                  textColor=colors.grey, alignment=1, spaceBefore=20)
    footer = Paragraph(
        "Data sourced from Yahoo Finance (delayed). Generated automatically with yfinance & reportlab.",
        footer_style
    )
    story.append(footer)

    # Build PDF
    doc.build(story)
    print(f"PDF report saved as → {filename}")

# -----------------------------
# 5. Run PDF export
# -----------------------------
export_pdf(top_winners, top_losers)
