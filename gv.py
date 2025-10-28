from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, HRFlowable # Import HRFlowable for horizontal line
from reportlab.lib.styles import ParagraphStyle

# Output file
pdf_file = "Samuel_Nathaniel_Data_Analyst_CV_Modern.pdf"

# Create PDF doc
doc = SimpleDocTemplate(pdf_file, pagesize=A4,
                        leftMargin=0.8*inch, rightMargin=0.8*inch,
                        topMargin=0.8*inch, bottomMargin=0.8*inch)

styles = getSampleStyleSheet()

# --- Custom Styles for Modern Design ---
# 1. Cleaner Title Font
title_style = ParagraphStyle('Title', fontName='Helvetica-Bold', fontSize=22, spaceAfter=2) # Larger font
# 2. Section Header with Accent Color and Line
header_style = ParagraphStyle('Header', fontName='Helvetica-Bold', fontSize=12, textColor=colors.HexColor("#1A5276"), spaceAfter=6, leftIndent=0)
# 3. Standard Body Text (for single lines and paragraphs)
body_style = ParagraphStyle('Body', fontName='Helvetica', fontSize=10, leading=14)
# 4. Reduced Bullet Style (for experience points only, using ReportLab's built-in list formatting is cleaner)
bullet_style_reduced = ParagraphStyle('Bullet', fontName='Helvetica', fontSize=10, leading=14, leftIndent=12)

# Custom flowable for a separator line
def get_separator():
    return HRFlowable(width="100%", thickness=0.5, lineCap='round', color=colors.HexColor("#A9A9A9"), spaceBefore=4, spaceAfter=8)

# Content list for the PDF
content = []

## 1. Header / Name Section
content.append(Paragraph("<b>Samuel Nathaniel</b>", title_style))
content.append(Paragraph("Uyo, Nigeria | sambless44@gmail.com", body_style))
content.append(Paragraph("LinkedIn: <a href='https://www.linkedin.com/in/samuel-n-0522171a0'>linkedin.com/in/samuel-n-0522171a0</a> | GitHub: <a href='https://github.com/BlissNathan1305'>github.com/BlissNathan1305</a>", body_style))
content.append(Spacer(1, 12))

# --- Modern Design: Professional Summary and Line Separator ---
content.append(Paragraph("PROFESSIONAL SUMMARY", header_style))
content.append(get_separator()) # Added separator line
content.append(Paragraph(
    "Analytical and detail-oriented <b>Data Analyst</b> with **2+ years of hands-on experience** in data wrangling, "
    "visualization, and statistical modeling. Experienced in extracting insights from complex datasets "
    "using **Python** and **R**, and in presenting actionable findings to support data-driven decisions. "
    "Proven track record of automating workflows, improving reporting speed, and translating raw data "
    "into impactful visual narratives that drive strategy.", body_style))
content.append(Spacer(1, 8))

# --- 2. Core Skills (Modern Design: Comma-Separated, No Bullets) ---
content.append(Paragraph("CORE SKILLS", header_style))
content.append(get_separator()) # Added separator line

skills_data = [
    ("Programming Languages", "Python, R"),
    ("Data Analysis Tools", "Pandas, NumPy, Matplotlib, Seaborn, ggplot2"),
    ("Data Visualization & BI", "Dashboards, Reports, Charts, **Power BI**"), 
    ("Statistical Techniques", "Hypothesis Testing, Regression, Correlation, ANOVA")
]

for category, items in skills_data:
    content.append(Paragraph(f"<b>{category}:</b> {items}", body_style))
content.append(Spacer(1, 8))


# --- 3. Technical Competencies (Modern Design: Comma-Separated, No Bullets) ---
content.append(Paragraph("TECHNICAL COMPETENCIES", header_style))
content.append(get_separator()) # Added separator line

competencies_data = [
    ("Database Management", "**SQL**, SQLite"),
    ("Version Control", "Git, GitHub"),
    ("Cloud Platform", "AWS (Data Storage and Processing)"),
    ("Workflow & Environment", "Jupyter Notebook, Google Colab, Excel, Kaggle, Notion")
]

for category, items in competencies_data:
    content.append(Paragraph(f"<b>{category}:</b> {items}", body_style))
content.append(Spacer(1, 8))


# --- 4. Professional Experience (Kept Bullets/Indentation for readability, but removed explicit '• ' prefix) ---
content.append(Paragraph("PROFESSIONAL EXPERIENCE", header_style))
content.append(get_separator()) # Added separator line
content.append(Paragraph("<b>Independent Data Analysis Consultant</b> | Freelance & Academic Projects — Remote (Jan 2023 – Present)", body_style))
experience_points = [
    "Analyzed and interpreted datasets of **10,000+ records** to identify performance trends and **inform strategic recommendations** for client projects.",
    "**Developed and automated** Python scripts that reduced data cleaning and processing time by **over 40%**.", 
    "**Designed and presented** dashboards and visual reports that improved stakeholder data understanding by **30%**.", 
    "Utilized Google Colab and Jupyter Notebook for reproducible, **well-documented workflows and model versioning**.",
    "Collaborated with Kaggle and GitHub communities to share and **validate novel data solutions**."
]
for e in experience_points:
    # We rely on the leftIndent in 'bullet_style_reduced' to provide the bullet effect if we use ListFlowable, 
    # but for simplicity and consistency, we'll keep it as indented paragraphs.
    content.append(Paragraph("• " + e, bullet_style_reduced)) 
    # Note: ReportLab uses ListFlowable to truly handle clean bullets, but for quick fix, 
    # we'll keep the indented paragraph structure but ensure the initial explicit '• ' is only added once here.
content.append(Spacer(1, 8))

# --- 5. Projects (Kept Bullets/Indentation for readability) ---
content.append(Paragraph("PROJECTS", header_style))
content.append(get_separator()) # Added separator line
projects = [
    "<b>Sales Performance Dashboard:</b> Built an interactive dashboard using Python (Matplotlib & Seaborn) to visualize sales metrics, improving reporting time by 25%.",
    "<b>Predictive Model for Customer Retention:</b> Developed a logistic regression model that improved accuracy by 15% through feature engineering.",
    "<b>COVID-19 Data Analysis (R):</b> Visualized global COVID-19 trends using ggplot2; delivered insights on infection rates and recovery."
]
for p in projects:
    content.append(Paragraph("• " + p, bullet_style_reduced))
content.append(Spacer(1, 8))

# --- 6. Certifications (Cleaned up) ---
content.append(Paragraph("CERTIFICATIONS", header_style))
content.append(get_separator()) # Added separator line
certs_list = [
    "Google Data Analytics Professional Certificate – Coursera", 
    "Data Analysis with Python – Coursera / IBM",
    "Introduction to R for Data Science – DataCamp / Kaggle"
]
for cert in certs_list:
    content.append(Paragraph(cert, body_style)) # Removed '• '
content.append(Spacer(1, 8))

# --- 7. Education (Cleaned up) ---
content.append(Paragraph("EDUCATION", header_style))
content.append(get_separator()) # Added separator line
content.append(Paragraph("<b>University of Uyo, Uyo</b>", body_style))
content.append(Paragraph("Master of Engineering (M.Eng.) in Agricultural Engineering – 2024", body_style)) # Removed '• '
content.append(Paragraph("Bachelor of Engineering (B.Eng.) in Agricultural Engineering – 2019", body_style)) # Removed '• '
content.append(Spacer(1, 8))

# --- 8. Soft Skills & Attributes (Condensed) ---
content.append(Paragraph("SOFT SKILLS & PROFESSIONAL ATTRIBUTES", header_style))
content.append(get_separator()) # Added separator line
attributes = "Critical Thinking • Problem Solving • Communication • Attention to Detail • Collaboration"
content.append(Paragraph(attributes, body_style))
content.append(Spacer(1, 8))

# Build the document
doc.build(content)

print(f"✅ Modern CV generated successfully: {pdf_file}")

