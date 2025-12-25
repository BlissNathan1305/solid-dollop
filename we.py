#!/usr/bin/env python3
"""
Daily Market Report → Colorful PDF
Indices: Dow Jones, S&P 500, NASDAQ-100
Most-active stocks (by volume)
Most-active options (proxy via high-volume underlyings)

PDF generated with reportlab – fully styled, easy to read.
"""

import yfinance as yf
import pandas as pd
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

# ---------- PDF generation ----------
from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT

# ---------- Web scraping ----------
import requests
from bs4 import BeautifulSoup

# ----------------------------------------------------------------------
# Helper: fetch most-active stocks from Yahoo Finance "Most Active" page
# ----------------------------------------------------------------------
def scrape_most_active_stocks(limit=10):
    url = "https://finance.yahoo.com/most-active"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")
    table = soup.find("table")
    df = pd.read_html(str(table))[0]

    # Keep only needed columns
    df = df[['Symbol', 'Name', 'Price (Intraday)', 'Change', '% Change', 'Volume (Intraday)']]
    df.columns = ['Symbol', 'Name', 'Price', 'Change', '% Change', 'Volume']
    df = df.head(limit)
    return df

# ----------------------------------------------------------------------
# 1. Indices
# ----------------------------------------------------------------------
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

# ----------------------------------------------------------------------
# 2. Most-active options (proxy)
# ----------------------------------------------------------------------
def get_most_active_options(limit=10):
    high_opt = ['SPY', 'QQQ', 'IWM', 'AAPL', 'TSLA', 'NVDA', 'AMD', 'AMC', 'META', 'AMZN']
    all_opts = []
    for sym in high_opt:
        try:
            t = yf.Ticker(sym)
            expirations = t.options
            if not expirations:
                continue
            exp = expirations[0]                     # nearest expiry
            chain = t.option_chain(exp)
            calls = chain.calls.copy()
            puts = chain.puts.copy()
            calls['type'] = 'Call'
            puts['type'] = 'Put'
            df = pd.concat([calls, puts], ignore_index=True)
            df['underlying'] = sym
            df['totalVolume'] = df['volume'].fillna(0).astype(int)
            all_opts.append(df)
        except Exception:
            continue
    if not all_opts:
        return pd.DataFrame()
    full = pd.concat(all_opts, ignore_index=True)
    top = full.sort_values('totalVolume', ascending=False).head(limit)
    return top[['underlying', 'strike', 'type', 'lastPrice', 'totalVolume', 'contractSymbol']]

# ----------------------------------------------------------------------
# PDF Builder
# ----------------------------------------------------------------------
def build_pdf(filename="Market_Report.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=LETTER,
                            rightMargin=0.75*inch, leftMargin=0.75*inch,
                            topMargin=1*inch, bottomMargin=0.75*inch)
    styles = getSampleStyleSheet()
    story = []

    # ---- Title ----
    title_style = ParagraphStyle(
        name='Title',
        parent=styles['Title'],
        fontSize=20,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#1a1a1a")
    )
    now = datetime.now().strftime("%B %d, %Y – %H:%M")
    story.append(Paragraph(f"Daily Market Report – {now}", title_style))
    story.append(Spacer(1, 0.2*inch))

    # ---- Helper to add a table with nice styling ----
    def add_table(df, title, col_widths=None, header_bg=colors.HexColor("#003366"),
                  row_colors=(colors.HexColor("#f9f9f9"), colors.white)):
        story.append(Paragraph(title, styles['Heading2']))
        story.append(Spacer(1, 0.08*inch))

        # Header row
        header = [[Paragraph(f"<b>{c}</b>", styles['Normal']) for c in df.columns]]
        data = header + df.values.tolist()

        t = Table(data, colWidths=col_widths)
        style_cmds = [
            ('BACKGROUND', (0, 0), (-1, 0), header_bg),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]
        # Alternate row colors
        for i in range(1, len(data)):
            bg = row_colors[i % 2]
            style_cmds.append(('BACKGROUND', (0, i), (-1, i), bg))
        t.setStyle(TableStyle(style_cmds))
        story.append(t)
        story.append(Spacer(1, 0.25*inch))

    # ---- 1. Indices ----
    idx_df = get_index_data()
    idx_df_styled = idx_df.copy()
    # Right-align numeric columns
    for col in ['Close', 'Change', '% Change', 'Volume']:
        idx_df_styled[col] = idx_df_styled[col].apply(lambda x: f"<para align=right>{x}</para>")
    add_table(idx_df_styled,
              "Major US Indices",
              col_widths=[3.2*inch, 1.1*inch, 1*inch, 0.9*inch, 1.2*inch],
              header_bg=colors.HexColor("#003366"))

    # ---- 2. Most-active stocks ----
    try:
        stocks_df = scrape_most_active_stocks(limit=12)
    except Exception as e:
        print("Warning: Scraping failed, using fallback tickers")
        stocks_df = pd.DataFrame()   # will be empty → fallback inside add_table

    if stocks_df.empty:
        # Fallback: popular high-volume tickers
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
                rows.append([s, name, f"{close:,.2f}", f"{chg:+,.2f}",
                             f"{pct:+.2f}%", f"{vol:,.0f}"])
            except: continue
        stocks_df = pd.DataFrame(rows,
                    columns=['Symbol','Name','Price','Change','% Change','Volume'])

    # Style numeric columns
    stock_styled = stocks_df.copy()
    for col in ['Price','Change','% Change','Volume']:
        stock_styled[col] = stock_styled[col].apply(lambda x: f"<para align=right>{x}</para>")
    add_table(stock_styled,
              "Top 12 Most Actively Traded Stocks (by Volume)",
              col_widths=[0.8*inch, 2.4*inch, 0.9*inch, 0.9*inch, 0.9*inch, 1.2*inch],
              header_bg=colors.HexColor("#006400"))

    # ---- 3. Most-active options ----
    opt_df = get_most_active_options(limit=12)
    if not opt_df.empty:
        opt_disp = opt_df.copy()
        opt_disp['Strike'] = opt_disp['strike'].apply(lambda x: f"{x:.2f}")
        opt_disp['Last'] = opt_disp['lastPrice'].apply(lambda x: f"{x:.2f}")
        opt_disp['Volume'] = opt_disp['totalVolume'].apply(lambda x: f"{x:,.0f}")
        opt_disp['Contract'] = opt_disp['contractSymbol'].str[-15:]
        opt_disp = opt_disp[['underlying','Strike','type','Last','Volume','Contract']]
        opt_disp.columns = ['Underlying','Strike','Type','Last','Volume','Contract']

        for col in ['Strike','Last','Volume']:
            opt_disp[col] = opt_disp[col].apply(lambda x: f"<para align=right>{x}</para>")

        add_table(opt_disp,
                  "Top 12 Most Active Options Contracts (Nearest Expiry)",
                  col_widths=[0.9*inch, 0.8*inch, 0.6*inch, 0.7*inch, 1*inch, 2*inch],
                  header_bg=colors.HexColor("#8B0000"))
    else:
        story.append(Paragraph("<b>Options data unavailable at this time.</b>", styles['Normal']))
        story.append(Spacer(1, 0.2*inch))

    # ---- Footer ----
    footer_style = ParagraphStyle(
        name='Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.grey,
        alignment=TA_CENTER,
        spaceBefore=30
    )
    footer = Paragraph(
        "Data sourced from Yahoo Finance (delayed). Generated automatically with yfinance & reportlab. "
        "For production use, consider official market-data providers.",
        footer_style)
    story.append(footer)

    # ---- Build PDF ----
    doc.build(story)
    print(f"PDF report saved as → {filename}")

# ----------------------------------------------------------------------
if __name__ == "__main__":
    build_pdf("Daily_Market_Report.pdf")
