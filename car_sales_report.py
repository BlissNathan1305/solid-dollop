#!/usr/bin/env python3
# car_sales_report.py
# Extracted top-20 sales data -> plots, PDF, HTML dashboard
# Requires: pandas, matplotlib, plotly
# Install missing packages: pip install pandas matplotlib plotly

import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

# Optional: plotly for interactive dashboard
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except Exception:
    PLOTLY_AVAILABLE = False

# --- Data (transcribed from image) ---
data = [
    (1, "Model Y (Tesla)", 15328),
    (2, "星愿 (Xingyuan)", 9016),
    (3, "Model 3 (Tesla)", 8644),
    (4, "小米 YU7 (Xiaomi)", 7299),
    (5, "海狮06 (Haishi06)", 6244),
    (6, "元UP (Yuan UP)", 5948),
    (7, "小米 SU7 (Xiaomi)", 5666),
    (8, "海豚 (Haitun / Dolphin)", 4988),
    (9, "海豹06 (Haibao06)", 4890),
    (10, "宝马3系 (BMW 3 Series)", 4837),
    (11, "途观L (Tiguan L)", 4799),
    (12, "问界M8 (Wenjie M8)", 4775),
    (13, "小鹏 MONA M03 (Xpeng)", 4357),
    (14, "凯美瑞 (Camry)", 4102),
    (15, "秦L (Qin L)", 3999),
    (16, "奔驰 C级 (Mercedes C-Class)", 3946),
    (17, "秦PLUS 新能源 (Qin PLUS NEV)", 3936),
    (18, "海鸥 (Seagull)", 3863),
    (19, "宏光 MINI EV (Hongguang MINI EV)", 3611),
    (20, "零跑 B01 (Leapmotor B01)", 3608),
]

df = pd.DataFrame(data, columns=["Rank", "Model", "Sales"])
df["Model_short"] = df["Model"].str.split(" ").str[0]

# Basic stats
stats = {
    "count": int(df["Sales"].count()),
    "sum": int(df["Sales"].sum()),
    "mean": float(df["Sales"].mean()),
    "median": float(df["Sales"].median()),
    "std": float(df["Sales"].std(ddof=0)),
    "min": int(df["Sales"].min()),
    "max": int(df["Sales"].max())
}

# Sort by sales descending and compute cumulative
df = df.sort_values("Sales", ascending=False).reset_index(drop=True)
df["Cumulative"] = df["Sales"].cumsum()
df["Cumulative_pct"] = 100 * df["Cumulative"] / df["Sales"].sum()

# Heuristic maker inference (edit as needed)
def infer_maker(model_string):
    s = model_string
    if "Model Y" in s or "Model 3" in s:
        return "Tesla"
    if "小米" in s or "YU7" in s or "SU7" in s:
        return "Xiaomi"
    if "小鹏" in s or "MONA" in s or "M03" in s:
        return "Xpeng"
    if "宝马" in s or "BMW" in s:
        return "BMW"
    if "途观" in s or "Tiguan" in s:
        return "Volkswagen"
    if "凯美瑞" in s:
        return "Toyota"
    if "奔驰" in s:
        return "Mercedes"
    if "秦" in s or "海" in s or "元UP" in s:
        if "问界" in s:
            return "AITO"
        return "BYD"
    if "宏光" in s:
        return "Wuling"
    if "零跑" in s:
        return "Leapmotor"
    if "星愿" in s:
        return "Unknown"
    return "Other"

df["Maker"] = df["Model"].apply(infer_maker)

# Aggregation by Maker
maker_summary = df.groupby("Maker")["Sales"].agg(["sum", "count"]).sort_values("sum", ascending=False).reset_index()

# Output directory
out_dir = os.path.join(os.getcwd(), "car_sales_report")
os.makedirs(out_dir, exist_ok=True)

# Save CSV
csv_path = os.path.join(out_dir, "top20_sales.csv")
df.to_csv(csv_path, index=False)

# Plot 1: Horizontal bar chart (models by sales)
plt.figure(figsize=(10, 8))
plt.barh(df["Model"], df["Sales"])
plt.gca().invert_yaxis()
plt.xlabel("Sales (units)")
plt.title("Top 20 Models by Sales (Ranked)")
plt.tight_layout()
fig1_path = os.path.join(out_dir, "bar_sales_by_model.png")
plt.savefig(fig1_path)
plt.close()

# Plot 2: Pie chart top 5 vs others
top5 = df.head(5)
others_sum = df["Sales"].iloc[5:].sum()
labels = list(top5["Model"]) + ["Others"]
sizes = list(top5["Sales"]) + [others_sum]
plt.figure(figsize=(7,7))
plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)
plt.title("Top 5 Models vs Others (Share)")
plt.tight_layout()
fig2_path = os.path.join(out_dir, "pie_top5_vs_others.png")
plt.savefig(fig2_path)
plt.close()

# Plot 3: Boxplot distribution
plt.figure(figsize=(6,6))
plt.boxplot(df["Sales"], vert=False)
plt.title("Sales Distribution (Top 20 models)")
plt.xlabel("Sales (units)")
plt.tight_layout()
fig3_path = os.path.join(out_dir, "boxplot_sales.png")
plt.savefig(fig3_path)
plt.close()

# Plot 4: Cumulative percentage curve
plt.figure(figsize=(10,6))
plt.plot(range(1, len(df)+1), df["Cumulative_pct"], marker='o')
plt.xticks(range(1, len(df)+1))
plt.xlabel("Model rank (1=highest sales)")
plt.ylabel("Cumulative % of total sales")
plt.title("Cumulative Sales Percentage by Rank")
plt.grid(True)
plt.tight_layout()
fig4_path = os.path.join(out_dir, "cumulative_pct.png")
plt.savefig(fig4_path)
plt.close()

# Create PDF report
pdf_path = os.path.join(out_dir, "car_sales_report.pdf")
with PdfPages(pdf_path) as pdf:
    fig = plt.figure(figsize=(11,8.5))
    fig.suptitle("Top 20 Model Sales Report - Extracted data", fontsize=18)
    plt.axis("off")
    plt.text(0.1, 0.6, f"Total models: {stats['count']}", fontsize=12)
    plt.text(0.1, 0.55, f"Total sales (sum): {stats['sum']}", fontsize=12)
    plt.text(0.1, 0.50, f"Mean sales: {stats['mean']:.1f}", fontsize=12)
    plt.text(0.1, 0.45, f"Median sales: {stats['median']:.1f}", fontsize=12)
    plt.text(0.1, 0.40, f"Sales standard deviation (population): {stats['std']:.1f}", fontsize=12)
    pdf.savefig(fig)
    plt.close(fig)
    # add the saved figures
    for fname in [fig1_path, fig2_path, fig3_path, fig4_path]:
        img = plt.imread(fname)
        fig = plt.figure(figsize=(11,8.5))
        plt.imshow(img)
        plt.axis("off")
        pdf.savefig(fig)
        plt.close(fig)

# Create interactive dashboard (Plotly) if available
dashboard_html = os.path.join(out_dir, "dashboard.html")
if PLOTLY_AVAILABLE:
    fig_bar = px.bar(df.sort_values("Sales", ascending=False), x="Sales", y="Model", orientation="h", title="Top 20 Models by Sales")
    fig_pie = px.pie(df, names="Model", values="Sales", title="Sales share by Model (Top 20)")
    fig_maker = px.bar(maker_summary, x="sum", y="Maker", orientation="h", title="Sales by Maker (aggregated)")
    with open(dashboard_html, "w", encoding="utf-8") as f:
        f.write("<html><head><meta charset='utf-8'><title>Car Sales Dashboard</title></head><body>")
        f.write("<h1>Car Sales Dashboard (Top 20)</h1>")
        f.write("<h2>Interactive Charts</h2>")
        f.write(fig_bar.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write("<hr>")
        f.write(fig_pie.to_html(full_html=False, include_plotlyjs=False))
        f.write("<hr>")
        f.write(fig_maker.to_html(full_html=False, include_plotlyjs=False))
        f.write("<hr>")
        f.write("<h2>Data Table</h2>")
        f.write(df.to_html(index=False))
        f.write("</body></html>")
else:
    # create a simple HTML page with static images and table
    with open(dashboard_html, "w", encoding="utf-8") as f:
        f.write("<html><head><meta charset='utf-8'><title>Car Sales Dashboard (static)</title></head><body>")
        f.write("<h1>Car Sales Dashboard (Top 20) - Static</h1>")
        f.write("<h2>Charts (images)</h2>")
        f.write(f"<img src='bar_sales_by_model.png' style='max-width:100%;'><br><hr>")
        f.write(f"<img src='pie_top5_vs_others.png' style='max-width:100%;'><br><hr>")
        f.write(f"<img src='boxplot_sales.png' style='max-width:100%;'><br><hr>")
        f.write(f"<img src='cumulative_pct.png' style='max-width:100%;'><br><hr>")
        f.write("<h2>Data Table</h2>")
        f.write(df.to_html(index=False))
        f.write("</body></html>")
    # copy images to out_dir (already saved there), nothing else required

# Summarize outputs
print("Created files in:", out_dir)
print(" - CSV:", csv_path)
print(" - PDF report:", pdf_path)
print(" - Dashboard (HTML):", dashboard_html)
print(" - Figures:", fig1_path, fig2_path, fig3_path, fig4_path)

