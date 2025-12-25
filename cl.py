#!/usr/bin/env python3
"""
Top 20 Most Traded US Penny Stocks → PDF
- Stocks under $5
- Sorted by daily trading volume
- PDF generated with reportlab
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
# 1. Define sample US tickers
# -----------------------------
# For production, you could scrape NASDAQ/OTC lists; here we use common penny-stock candidates
tickers = [
    "AMC", "GME", "NIO", "SNDL", "BB", "FUBO", "PLTR", "AAL", "EXPR", "KOSS",
    "SIRI", "RIOT", "CLNE", "MNKD", "TRVG", "CLOV", "AUPH", "NOK", "SPCE", "FCEL",
    "AGNC", "NVAX", "F", "BBBY", "SOS", "IQ"
]

# -----------------------------
# 2. Fetch price & volume
# -----------------------------
data = []
for ticker in tickers:
    try:
        t = yf.Ticker(ticker)
        hist = t.history(period="1d")
        if hist.empty:
            continue  # Skip delisted/no data
        close = hist['Close'].iloc[-1]
        volume = hist['Volume'].iloc[-1]
        if close < 5:  # Penny stock filter
            data.append([ticker, f"${close:.2f}", f"{volume:,}"])
    except Exception:
        continue

# -----------------------------
# 3. Sort by volume, top 20
# -----------------------------
df = pd.DataFrame(data, columns=["Ticker", "Price", "Volume"])
df = df.sort_values("Volume", ascending=False).head(20)

# -----------------------------
# 4. Export to PDF
# -----------------------------
def export_pdf(df, filename="Top_20_Penny_Stocks.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=LETTER,
                            rightMargin=0.75*inch, leftMargin=0.75*inch,
                            topMargin=1*inch, bottomMargin=0.75*inch)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Title'],
        fontSize=22,
        spaceAfter=20,
        alignment=1,  # center
        textColor=colors.HexColor("#0B3D91")
    )
    now = datetime.now().strftime("%B %d, %Y – %H:%M")
    story.append(Paragraph(f"Top 20 Most Traded US Penny Stocks – {now}", title_style))
    story.append(Spacer(1, 0.2*inch))

    # Table
    header = [[Paragraph(f"<b>{c}</b>", styles['Normal']) for c in df.columns]]
    data_table = header + df.values.tolist()
    table = Table(data_table, hAlign='CENTER', colWidths=[1.5*inch, 1.2*inch, 1.5*inch])
    style_cmds = [
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#006400")),
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

    # Footer
    footer_style = ParagraphStyle('Footer', parent=styles['Normal'], fontSize=9,
                                  textColor=colors.grey, alignment=1, spaceBefore=20)
    footer = Paragraph(
        "Data sourced from Yahoo Finance (delayed). Generated automatically with yfinance & reportlab.",
        footer_style
    )
    story.append(Spacer(1, 0.3*inch))
    story.append(footer)

    doc.build(story)
    print(f"PDF report saved as → {filename}")

# -----------------------------
# 5. Run PDF export
# -----------------------------
export_pdf(df)
