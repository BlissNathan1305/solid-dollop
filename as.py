import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
from datetime import date

# --- 1️⃣ Define assets ---
stocks = ["AAPL", "MSFT", "TSLA", "NVDA", "AMZN", "GOOG"]
futures = ["GC=F", "CL=F", "ES=F", "NQ=F"]   # Gold, Oil, S&P 500, Nasdaq
cryptos = ["BTC-USD", "ETH-USD"]

all_assets = stocks + futures + cryptos

# --- 2️⃣ Download weekly data safely ---
data = yf.download(all_assets, period="7d", interval="1d", group_by='ticker')

# --- 3️⃣ Extract Adjusted Close safely ---
adj_close = pd.DataFrame()
for ticker in all_assets:
    try:
        # Some tickers (like crypto) might have only 'Close', not 'Adj Close'
        if 'Adj Close' in data[ticker]:
            adj_close[ticker] = data[ticker]['Adj Close']
        else:
            adj_close[ticker] = data[ticker]['Close']
    except KeyError:
        print(f"Warning: Could not find data for {ticker}")

# --- 4️⃣ Drop any columns that are completely NaN ---
adj_close = adj_close.dropna(axis=1, how='all')

# --- 5️⃣ Calculate weekly performance ---
performance = (adj_close.iloc[-1] - adj_close.iloc[0]) / adj_close.iloc[0] * 100
performance = performance.sort_values(ascending=False)

# --- 6️⃣ Identify top performer ---
top_asset = performance.index[0]
top_value = performance.iloc[0]

# --- 7️⃣ Create performance chart ---
plt.figure(figsize=(10,5))
bars = plt.bar(performance.index, performance.values, color="skyblue")
# Highlight best performer
bars[0].set_color("green")
plt.title("Weekly Market Performance (%)")
plt.ylabel("Percentage Change (%)")
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig("weekly_performance.png")
plt.close()

# --- 8️⃣ Prepare summary DataFrame ---
summary = pd.DataFrame({
    "Asset": performance.index,
    "Performance (%)": performance.values.round(2)
})

# --- 9️⃣ Generate PDF report ---
pdf = FPDF()
pdf.add_page()
pdf.set_font("Helvetica", "B", 16)
pdf.cell(0, 10, "Weekly Market Performance Report", ln=True, align="C")
pdf.ln(8)
pdf.set_font("Helvetica", "", 12)
pdf.cell(0, 8, f"Report Date: {date.today()}", ln=True)
pdf.ln(5)

pdf.multi_cell(0, 8, f"Top Performer: {top_asset} ({top_value:.2f}%)", align="L")
pdf.ln(5)

pdf.set_font("Helvetica", "B", 12)
pdf.cell(0, 8, "Performance Summary:", ln=True)
pdf.set_font("Helvetica", "", 11)
for i, row in summary.iterrows():
    line = f"{row['Asset']:<10} {row['Performance (%)']:>10}%"
    pdf.cell(0, 8, line, ln=True)

pdf.ln(10)
pdf.image("weekly_performance.png", x=15, y=None, w=180)
pdf.ln(10)

pdf.set_font("Helvetica", "I", 10)
pdf.cell(0, 10, "Data Source: Yahoo Finance", ln=True, align="C")

pdf.output("weekly_market_report.pdf")

print("✅ Report generated successfully: weekly_market_report.pdf")
