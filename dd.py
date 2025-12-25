#!/usr/bin/env python3
"""
SNAP Issuance Statistical Analysis and Visualization Dashboard
Generates comprehensive insights and exports to PDF
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
from datetime import datetime

# Set style for better visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (11, 8.5)
plt.rcParams['font.size'] = 9

# SNAP Issuance Data
data = """State	FY-2019 Issuance	FY-2020 Issuance	FY-2021 Issuance	
Alabama	1,032,064,886	1,347,837,969	1,974,053,519	
Alaska	171,091,672	198,298,993	288,045,258	
Arizona	1,146,712,214	1,469,287,888	2,175,824,745	
Arkansas	460,333,605	661,575,029	765,794,046	
California	5,977,281,299	7,822,153,332	11,243,441,465	
Colorado	639,000,457	905,796,877	1,304,761,706	
Connecticut	584,718,600	712,241,439	980,157,323	
Delaware	178,138,585	215,099,909	288,020,710	
District of Columbia	172,078,913	225,271,944	381,121,744	
Florida	4,035,386,245	6,001,741,105	8,089,425,782	
Georgia	2,115,101,241	2,907,470,344	4,085,504,054	
Guam	100,147,900	114,630,516	134,063,683	
Hawaii	448,431,408	564,142,303	944,131,080	
Idaho	192,918,233	241,620,261	258,375,969	
Illinois	2,646,035,880	3,392,686,172	5,104,129,949	
Indiana	819,644,875	1,170,741,466	1,619,482,193	
Iowa	429,300,000	530,239,443	727,003,000	
Kansas	395,405,972	488,510,000	513,500,000	
Kentucky	829,000,000	1,001,025,648	1,610,000,000	
Louisiana	1,214,657,000	1,536,165,366	2,462,000,000	
Maine	203,630,527	277,021,739	409,966,690	
Maryland	878,649,666	1,270,867,932	2,146,479,444	
Massachusetts	1,131,148,466	1,473,489,182	2,350,041,332	
Michigan	1,701,430,344	2,305,174,756	3,246,391,707	
Minnesota	509,464,759	724,808,065	1,985,655,426	
Mississippi	605,780,127	774,433,886	1,066,435,430	
Missouri	996,212,141	1,342,772,664	1,734,889,161	
Montana	146,944,184	185,184,948	228,795,841	
Nebraska	221,960,791	255,735,193	356,554,249	
Nevada	587,953,503	806,791,226	1,085,383,815	
New Hampshire	92,889,191	117,255,288	174,557,213	
New Jersey	953,558,696	1,288,738,288	2,169,432,714	
New Mexico	632,907,856	850,575,322	1,339,883,626	
New York	4,339,617,966	5,118,688,449	7,311,543,597	
North Carolina	1,863,656,810	2,396,397,649	3,994,650,815	
North Dakota	68,485,818	84,959,987	113,160,074	
Ohio	2,020,497,444	2,751,849,221	3,865,203,855	
Oklahoma	819,546,294	1,056,255,266	1,502,065,758	
Oregon	884,189,650	1,295,970,159	1,847,403,478	
Pennsylvania	2,513,696,584	3,249,170,461	5,170,214,891	
Rhode Island	244,223,564	280,718,378	378,689,563	
South Carolina	854,652,751	1,101,825,493	1,550,266,093	
South Dakota	121,995,672	143,855,862	177,819,200	
Tennessee	1,307,248,122	1,964,487,295	3,094,821,635	
Texas	4,767,112,796	6,282,102,824	8,751,945,285	
Utah	234,552,832	281,260,645	412,957,155	
Vermont	100,248,674	146,353,926	169,354,925	
Virginia	1,002,380,166	1,331,022,986	1,901,832,165	
Virgin Islands	45,039,243	53,574,541	79,508,500	
Washington	1,192,380,309	1,598,425,639	2,359,661,930	
West Virginia	397,899,950	516,954,512	772,297,950	
Wisconsin	778,373,061	1,108,618,259	1,964,034,853	
Wyoming	36,277,115	45,887,728	73,313,685"""

# Parse data using heredoc-style approach
from io import StringIO
df = pd.read_csv(StringIO(data), sep='\t', thousands=',')

# Remove any empty columns
df = df.dropna(axis=1, how='all')

# Clean column names - handle extra columns
if len(df.columns) > 4:
    df = df.iloc[:, :4]  # Keep only first 4 columns

df.columns = ['State', 'FY2019', 'FY2020', 'FY2021']

# Calculate additional metrics
df['Total_Issuance'] = df[['FY2019', 'FY2020', 'FY2021']].sum(axis=1)
df['Growth_2019_2020'] = ((df['FY2020'] - df['FY2019']) / df['FY2019'] * 100)
df['Growth_2020_2021'] = ((df['FY2021'] - df['FY2020']) / df['FY2020'] * 100)
df['Total_Growth'] = ((df['FY2021'] - df['FY2019']) / df['FY2019'] * 100)
df['Avg_Annual_Issuance'] = df['Total_Issuance'] / 3

# Statistical Summary
stats_summary = {
    'FY2019': df['FY2019'].describe(),
    'FY2020': df['FY2020'].describe(),
    'FY2021': df['FY2021'].describe()
}

# Create PDF with multiple pages
pdf_filename = 'SNAP_Issuance_Analysis_Dashboard.pdf'
with PdfPages(pdf_filename) as pdf:
    
    # PAGE 1: Title and Executive Summary
    fig = plt.figure(figsize=(11, 8.5))
    fig.suptitle('SNAP Issuance Analysis Dashboard\nFY 2019-2021', 
                 fontsize=20, fontweight='bold', y=0.95)
    
    ax = fig.add_subplot(111)
    ax.axis('off')
    
    summary_text = f"""
    EXECUTIVE SUMMARY
    
    Analysis Period: FY 2019 - FY 2021
    Generated: {datetime.now().strftime('%B %d, %Y')}
    
    KEY FINDINGS:
    
    • Total SNAP Issuance (All States, 3 Years): ${df['Total_Issuance'].sum():,.0f}
    
    • National Year-over-Year Growth:
      - FY 2019 → 2020: {df['Growth_2019_2020'].mean():.1f}% average increase
      - FY 2020 → 2021: {df['Growth_2020_2021'].mean():.1f}% average increase
      - Overall Growth (2019-2021): {df['Total_Growth'].mean():.1f}% average
    
    • Top 5 States by Total Issuance (FY 2019-2021):
      1. {df.nlargest(1, 'Total_Issuance').iloc[0]['State']}: ${df.nlargest(1, 'Total_Issuance').iloc[0]['Total_Issuance']:,.0f}
      2. {df.nlargest(2, 'Total_Issuance').iloc[1]['State']}: ${df.nlargest(2, 'Total_Issuance').iloc[1]['Total_Issuance']:,.0f}
      3. {df.nlargest(3, 'Total_Issuance').iloc[2]['State']}: ${df.nlargest(3, 'Total_Issuance').iloc[2]['Total_Issuance']:,.0f}
      4. {df.nlargest(4, 'Total_Issuance').iloc[3]['State']}: ${df.nlargest(4, 'Total_Issuance').iloc[3]['Total_Issuance']:,.0f}
      5. {df.nlargest(5, 'Total_Issuance').iloc[4]['State']}: ${df.nlargest(5, 'Total_Issuance').iloc[4]['Total_Issuance']:,.0f}
    
    • Highest Growth States (FY 2019-2021):
      1. {df.nlargest(1, 'Total_Growth').iloc[0]['State']}: {df.nlargest(1, 'Total_Growth').iloc[0]['Total_Growth']:.1f}%
      2. {df.nlargest(2, 'Total_Growth').iloc[1]['State']}: {df.nlargest(2, 'Total_Growth').iloc[1]['Total_Growth']:.1f}%
      3. {df.nlargest(3, 'Total_Growth').iloc[2]['State']}: {df.nlargest(3, 'Total_Growth').iloc[2]['Total_Growth']:.1f}%
    
    INSIGHTS:
    
    • Significant increase in SNAP issuance across all states from 2019 to 2021,
      likely reflecting economic impacts of the COVID-19 pandemic
    
    • Large states (CA, TX, FL, NY) dominate total issuance volumes
    
    • Growth rates vary significantly by state, indicating different regional
      economic impacts and policy responses
    """
    
    ax.text(0.1, 0.5, summary_text, fontsize=11, verticalalignment='center',
            fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()
    
    # PAGE 2: Top 15 States by Total Issuance
    fig, ax = plt.subplots(figsize=(11, 8.5))
    top15 = df.nlargest(15, 'Total_Issuance')
    
    x = np.arange(len(top15))
    width = 0.25
    
    bars1 = ax.bar(x - width, top15['FY2019']/1e9, width, label='FY 2019', alpha=0.8)
    bars2 = ax.bar(x, top15['FY2020']/1e9, width, label='FY 2020', alpha=0.8)
    bars3 = ax.bar(x + width, top15['FY2021']/1e9, width, label='FY 2021', alpha=0.8)
    
    ax.set_xlabel('State', fontweight='bold', fontsize=12)
    ax.set_ylabel('SNAP Issuance (Billions $)', fontweight='bold', fontsize=12)
    ax.set_title('Top 15 States by Total SNAP Issuance (FY 2019-2021)', 
                 fontweight='bold', fontsize=14, pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(top15['State'], rotation=45, ha='right')
    ax.legend(loc='upper right')
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()
    
    # PAGE 3: Growth Rate Analysis
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 8.5))
    
    # Top 15 by growth rate
    top_growth = df.nlargest(15, 'Total_Growth')
    ax1.barh(top_growth['State'], top_growth['Total_Growth'], color='steelblue', alpha=0.7)
    ax1.set_xlabel('Total Growth Rate (%)', fontweight='bold')
    ax1.set_title('Top 15 States by Growth Rate (FY 2019-2021)', fontweight='bold', fontsize=12)
    ax1.grid(axis='x', alpha=0.3)
    
    # Year-over-year growth comparison
    growth_comparison = df.nlargest(10, 'Total_Issuance')[['State', 'Growth_2019_2020', 'Growth_2020_2021']]
    x = np.arange(len(growth_comparison))
    width = 0.35
    
    ax2.bar(x - width/2, growth_comparison['Growth_2019_2020'], width, 
            label='2019→2020', alpha=0.8, color='coral')
    ax2.bar(x + width/2, growth_comparison['Growth_2020_2021'], width, 
            label='2020→2021', alpha=0.8, color='lightseagreen')
    
    ax2.set_xlabel('State', fontweight='bold')
    ax2.set_ylabel('Growth Rate (%)', fontweight='bold')
    ax2.set_title('Year-over-Year Growth: Top 10 States by Total Issuance', 
                  fontweight='bold', fontsize=12)
    ax2.set_xticks(x)
    ax2.set_xticklabels(growth_comparison['State'], rotation=45, ha='right')
    ax2.legend()
    ax2.grid(axis='y', alpha=0.3)
    ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    
    plt.tight_layout()
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()
    
    # PAGE 4: Statistical Distribution
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(11, 8.5))
    fig.suptitle('Statistical Distribution Analysis', fontweight='bold', fontsize=14)
    
    # Box plots for each year
    data_to_plot = [df['FY2019']/1e6, df['FY2020']/1e6, df['FY2021']/1e6]
    bp = ax1.boxplot(data_to_plot, labels=['FY 2019', 'FY 2020', 'FY 2021'], patch_artist=True)
    for patch in bp['boxes']:
        patch.set_facecolor('lightblue')
    ax1.set_ylabel('SNAP Issuance (Millions $)', fontweight='bold')
    ax1.set_title('Distribution by Fiscal Year', fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    
    # Histogram of FY 2021
    ax2.hist(df['FY2021']/1e6, bins=20, color='steelblue', alpha=0.7, edgecolor='black')
    ax2.set_xlabel('SNAP Issuance (Millions $)', fontweight='bold')
    ax2.set_ylabel('Number of States', fontweight='bold')
    ax2.set_title('FY 2021 Issuance Distribution', fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    # Scatter plot: FY2019 vs FY2021
    ax3.scatter(df['FY2019']/1e6, df['FY2021']/1e6, alpha=0.6, s=50)
    ax3.set_xlabel('FY 2019 Issuance (Millions $)', fontweight='bold')
    ax3.set_ylabel('FY 2021 Issuance (Millions $)', fontweight='bold')
    ax3.set_title('FY 2019 vs FY 2021 Comparison', fontweight='bold')
    
    # Add diagonal line
    max_val = max(df['FY2021'].max(), df['FY2019'].max()) / 1e6
    ax3.plot([0, max_val], [0, max_val], 'r--', alpha=0.5, label='Equal Line')
    ax3.legend()
    ax3.grid(alpha=0.3)
    
    # Growth rate distribution
    ax4.hist(df['Total_Growth'], bins=20, color='coral', alpha=0.7, edgecolor='black')
    ax4.set_xlabel('Total Growth Rate (%)', fontweight='bold')
    ax4.set_ylabel('Number of States', fontweight='bold')
    ax4.set_title('Growth Rate Distribution (2019-2021)', fontweight='bold')
    ax4.axvline(x=df['Total_Growth'].mean(), color='red', linestyle='--', 
                linewidth=2, label=f'Mean: {df["Total_Growth"].mean():.1f}%')
    ax4.legend()
    ax4.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()
    
    # PAGE 5: Regional Analysis (Pie Chart and Heatmap)
    fig = plt.figure(figsize=(11, 8.5))
    fig.suptitle('Regional and Comparative Analysis', fontweight='bold', fontsize=14)
    
    # Top 10 states pie chart for FY 2021
    ax1 = plt.subplot(2, 2, (1, 2))
    top10_fy2021 = df.nlargest(10, 'FY2021')
    others = df.nsmallest(len(df) - 10, 'FY2021')['FY2021'].sum()
    
    pie_data = list(top10_fy2021['FY2021']) + [others]
    pie_labels = list(top10_fy2021['State']) + ['Others']
    
    colors = plt.cm.Set3(np.linspace(0, 1, len(pie_data)))
    ax1.pie(pie_data, labels=pie_labels, autopct='%1.1f%%', startangle=90, colors=colors)
    ax1.set_title('FY 2021 Issuance Share (Top 10 States + Others)', fontweight='bold', pad=20)
    
    # Heatmap of year-over-year data for top 20 states
    ax2 = plt.subplot(2, 1, 2)
    top20 = df.nlargest(20, 'Total_Issuance')
    heatmap_data = top20[['FY2019', 'FY2020', 'FY2021']].T
    heatmap_data.columns = top20['State']
    
    # Normalize for better visualization
    heatmap_normalized = (heatmap_data - heatmap_data.min()) / (heatmap_data.max() - heatmap_data.min())
    
    im = ax2.imshow(heatmap_normalized, aspect='auto', cmap='YlOrRd')
    ax2.set_xticks(np.arange(len(top20)))
    ax2.set_yticks(np.arange(3))
    ax2.set_xticklabels(top20['State'], rotation=45, ha='right', fontsize=8)
    ax2.set_yticklabels(['FY 2019', 'FY 2020', 'FY 2021'])
    ax2.set_title('Normalized Issuance Heatmap (Top 20 States)', fontweight='bold', pad=10)
    
    plt.colorbar(im, ax=ax2, label='Normalized Issuance')
    
    plt.tight_layout()
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()
    
    # PAGE 6: Statistical Summary Table
    fig, ax = plt.subplots(figsize=(11, 8.5))
    ax.axis('tight')
    ax.axis('off')
    
    fig.suptitle('Statistical Summary Tables', fontweight='bold', fontsize=14, y=0.98)
    
    # Summary statistics
    summary_data = []
    for year in ['FY2019', 'FY2020', 'FY2021']:
        summary_data.append([
            year,
            f"${df[year].sum()/1e9:.2f}B",
            f"${df[year].mean()/1e6:.2f}M",
            f"${df[year].median()/1e6:.2f}M",
            f"${df[year].std()/1e6:.2f}M",
            f"${df[year].min()/1e6:.2f}M",
            f"${df[year].max()/1e9:.2f}B"
        ])
    
    table1 = ax.table(cellText=summary_data,
                     colLabels=['Year', 'Total', 'Mean', 'Median', 'Std Dev', 'Min', 'Max'],
                     cellLoc='center',
                     loc='upper center',
                     bbox=[0.1, 0.7, 0.8, 0.25])
    table1.auto_set_font_size(False)
    table1.set_fontsize(10)
    table1.scale(1, 2)
    
    # Style header
    for i in range(7):
        table1[(0, i)].set_facecolor('#4CAF50')
        table1[(0, i)].set_text_props(weight='bold', color='white')
    
    # Top/Bottom performers
    performers_data = []
    top5 = df.nlargest(5, 'Total_Growth')
    bottom5 = df.nsmallest(5, 'Total_Growth')
    
    ax.text(0.5, 0.6, 'Top 5 Growth States (2019-2021)', 
            ha='center', fontweight='bold', fontsize=12, transform=ax.transAxes)
    
    for idx, row in top5.iterrows():
        performers_data.append([row['State'], f"{row['Total_Growth']:.1f}%"])
    
    table2 = ax.table(cellText=performers_data,
                     colLabels=['State', 'Growth Rate'],
                     cellLoc='center',
                     loc='center',
                     bbox=[0.1, 0.35, 0.35, 0.2])
    table2.auto_set_font_size(False)
    table2.set_fontsize(9)
    
    for i in range(2):
        table2[(0, i)].set_facecolor('#2196F3')
        table2[(0, i)].set_text_props(weight='bold', color='white')
    
    ax.text(0.5, 0.3, 'Bottom 5 Growth States (2019-2021)', 
            ha='center', fontweight='bold', fontsize=12, transform=ax.transAxes)
    
    performers_data2 = []
    for idx, row in bottom5.iterrows():
        performers_data2.append([row['State'], f"{row['Total_Growth']:.1f}%"])
    
    table3 = ax.table(cellText=performers_data2,
                     colLabels=['State', 'Growth Rate'],
                     cellLoc='center',
                     loc='center',
                     bbox=[0.55, 0.35, 0.35, 0.2])
    table3.auto_set_font_size(False)
    table3.set_fontsize(9)
    
    for i in range(2):
        table3[(0, i)].set_facecolor('#FF9800')
        table3[(0, i)].set_text_props(weight='bold', color='white')
    
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()
    
    # Set PDF metadata
    d = pdf.infodict()
    d['Title'] = 'SNAP Issuance Analysis Dashboard FY 2019-2021'
    d['Author'] = 'Data Analysis System'
    d['Subject'] = 'Statistical Analysis and Visualization'
    d['Keywords'] = 'SNAP, Food Assistance, Statistical Analysis, Dashboard'
    d['CreationDate'] = datetime.now()

print(f"✓ Analysis complete! Dashboard exported to: {pdf_filename}")
print(f"✓ Total pages: 6")
print(f"✓ States analyzed: {len(df)}")
print(f"✓ Time period: FY 2019 - FY 2021")
