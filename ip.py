#!/usr/bin/env python3
"""
Global Market Report → Colorful PDF
Includes:
- Major US Indices: Dow Jones, S&P 500, NASDAQ-100
- Top Most-Active Stocks (by volume)
- Top Most-Active Options Contracts (nearest expiry)

PDF generated with reportlab – fully styled, readable, and modern.
"""

import yfinance as yf
import pandas as pd
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER

import requests
from bs4 import BeautifulSoup

# -------------------------------
# 1. Fetch Most-Active Stocks
# -------------------------------
def scrape_most_active_stocks(limit=10):
    try:
        url = "https://finance.yahoo.com/most-active"
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")
        table = soup.find("table")
        df = pd.read_html(str(table))[0]

        df = df[['Symbol', 'Name', 'Price (Intraday)', 'Change', '% Change', 'Volume (Intraday)']]
        df.columns = ['Symbol', 'Name', 'Price', 'Change', '% Change', 'Volume']
        return df.head(limit)
    except Exception:
        return pd.DataFrame()

# -------------------------------
# 2. Major Indices Data
# -------------------------------
def get_index_data():
    indices = {
        '^DJI': 'Dow Jones Industrial Average',
        '^GSPC': 'S&P 500',
        '^NDX': 'NASDAQ 100'
    }
    rows = []
    for symbol, name in indices.items():
        try:
            t = yf.Ticker(symbol)
            hist = t.history(period="2d")
            if len(hist) < 2:
                continue
            close = hist['Close'].iloc[-1]
            prev = hist['Close'].iloc[-2]
            change = close - prev
            pct = change / prev * 100
            vol = hist['Volume'].iloc[-1]
            rows.append([name, f"{close:,.2f}", f"{change:+,.2f}", f"{pct:+.2f}%", f"{vol:,.0f}"])
        except Exception:
            rows.append([name, "N/A", "N/A", "N/A", "N/A"])
    return pd.DataFrame(rows, columns=['Index', 'Close', 'Change', '% Change', 'Volume'])

# -------------------------------
# 3. Most-Active Options
# -------------------------------
def get_most_active_options(limit=10):
    symbols = ['SPY','QQQ','IWM','AAPL','TSLA','NVDA','AMD','AMC','META','AMZN']
    all_opts = []
    for sym in symbols:
        try:
            t = yf.Ticker(sym)
            if not t.options:
                continue
            exp = t.options[0]  # nearest expiry
            chain = t.option_chain(exp)
            calls = chain.calls.copy(); calls['Type'] = 'Call'
            puts = chain.puts.copy(); puts['Type'] = 'Put'
            df = pd.concat([calls, puts], ignore_index=True)
            df['Underlying'] = sym
            df['Volume'] = df['volume'].fillna(0).astype(int)
            all_opts.append(df)
        except Exception:
            continue
    if not all_opts:
        return pd.DataFrame()
    full = pd.concat(all_opts, ignore_index=True)
    top = full.sort_values('Volume', ascending=False).head(limit)
    top = top[['Underlying','strike','Type','lastPrice','Volume','contractSymbol']]
    top.columns = ['Underlying','Strike','Type','Last','Volume','Contract']
    return top

# -------------------------------
# 4. PDF Builder
# -------------------------------
def build_pdf(filename="Global_Market_Report.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=LETTER,
                            rightMargin=0.75*inch, leftMargin=0.75*inch,
                            topMargin=1*inch, bottomMargin=0.75*inch)
    styles = getSampleStyleSheet()
    story = []

    # ---- Title ----
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Title'],
        fontSize=22,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#0B3D91")
    )
    now = datetime.now().strftime("%B %d, %Y – %H:%M")
    story.append(Paragraph(f"Global Market Report – {now}", title_style))
    story.append(Spacer(1, 0.2*inch))

    # ---- Table Helper ----
    def add_table(df, title, header_bg=colors.HexColor("#0B3D91"), row_colors=(colors.HexColor("#f9f9f9"), colors.white)):
        story.append(Paragraph(title, styles['Heading2']))
        story.append(Spacer(1, 0.1*inch))
        header = [[Paragraph(f"<b>{c}</b>", styles['Normal']) for c in df.columns]]
        data = header + df.values.tolist()
        t = Table(data, hAlign='CENTER')
        style_cmds = [
            ('BACKGROUND', (0,0), (-1,0), header_bg),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ]
        for i in range(1, len(data)):
            bg = row_colors[i % 2]
            style_cmds.append(('BACKGROUND', (0,i), (-1,i), bg))
        t.setStyle(TableStyle(style_cmds))
        story.append(t)
        story.append(Spacer(1, 0.25*inch))

    # ---- Major Indices ----
    idx_df = get_index_data()
    add_table(idx_df, "Major US Indices")

    # ---- Most-Active Stocks ----
    stocks_df = scrape_most_active_stocks(limit=12)
    if stocks_df.empty:
        fallback = ['AAPL','TSLA','NVDA','AMD','AMC','GME','SPY','QQQ','T','F']
        rows = []
        for s in fallback:
            try:
                t = yf.Ticker(s)
                info = t.info
                hist = t.history(period="1d")
                if hist.empty: continue
                close = hist['Close'].iloc[-1]
                vol = hist['Volume'].iloc[-1]
                prev = info.get('previousClose', close)
                chg = close - prev
                pct = chg/prev*100 if prev else 0
                name = (info.get('longName') or s)[:30]
                rows.append([s, name, f"{close:,.2f}", f"{chg:+,.2f}", f"{pct:+.2f}%", f"{vol:,.0f}"])
            except: continue
        stocks_df = pd.DataFrame(rows, columns=['Symbol','Name','Price','Change','% Change','Volume'])
    add_table(stocks_df, "Top 12 Most Actively Traded Stocks (by Volume)", header_bg=colors.HexColor("#006400"))

    # ---- Most-Active Options ----
    opt_df = get_most_active_options(limit=12)
    if not opt_df.empty:
        add_table(opt_df, "Top 12 Most Active Options Contracts (Nearest Expiry)", header_bg=colors.HexColor("#8B0000"))
    else:
        story.append(Paragraph("<b>Options data unavailable at this time.</b>", styles['Normal']))
        story.append(Spacer(1, 0.2*inch))

    # ---- Footer ----
    footer_style = ParagraphStyle('Footer', parent=styles['Normal'], fontSize=9, textColor=colors.grey, alignment=TA_CENTER, spaceBefore=20)
    footer = Paragraph(
        "Data sourced from Yahoo Finance (delayed). Generated automatically with yfinance & reportlab.",
        footer_style
    )
    story.append(footer)

    doc.build(story)
    print(f"PDF report saved as → {filename}")

# -------------------------------
if __name__ == "__main__":
    build_pdf("Global_Market_Report.pdf")
