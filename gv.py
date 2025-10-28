from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer # Correct import
from reportlab.lib.styles import ParagraphStyle

# Output file
pdf_file = "Samuel_Nathaniel_Data_Analyst_CV_Optimized.pdf"

# Create PDF doc - CORRECTION HERE: SimpleDocDocTemplate -> SimpleDocTemplate
doc = SimpleDocTemplate(pdf_file, pagesize=A4, 
                        leftMargin=0.8*inch, rightMargin=0.8*inch,
                        topMargin=0.8*inch, bottomMargin=0.8*inch)

styles = getSampleStyleSheet()

# Custom styles (Kept consistent)
title_style = ParagraphStyle('Title', fontName='Helvetica-Bold', fontSize=18, spaceAfter=10)
header_style = ParagraphStyle('Header', fontName='Helvetica-Bold', fontSize=12, textColor=colors.HexColor("#1A5276"), spaceAfter=6)
body_style = ParagraphStyle('Body', fontName='Helvetica', fontSize=10, leading=14)
bullet_style = ParagraphStyle('Bullet', fontName='Helvetica', fontSize=10, leading=14, leftIndent=12)

# Content list for the PDF
content = []

## 1. Header / Name Section (No change)
content.append(Paragraph("<b>Samuel Nathaniel</b>", title_style))
content.append(Paragraph("Uyo, Nigeria | sambless44@gmail.com", body_style))
content.append(Paragraph("LinkedIn: <a href='https://www.linkedin.com/in/samuel-n-0522171a0'>linkedin.com/in/samuel-n-0522171a0</a>", body_style))
content.append(Paragraph("GitHub: <a href='https://github.com/BlissNathan1305'>github.com/BlissNathan1305</a>", body_style))
content.append(Spacer(1, 12))

## 2. Professional Summary (Improved: Added quantifiable experience and stronger verbs)
content.append(Paragraph("PROFESSIONAL SUMMARY", header_style))
content.append(Paragraph(
    "Analytical and detail-oriented <b>Data Analyst</b> with **2+ years of hands-on experience** in data wrangling, "
    "visualization, and statistical modeling. Experienced in extracting insights from complex datasets "
    "using **Python** and **R**, and in presenting actionable findings to support data-driven decisions. "
    "Proven track record of automating workflows, improving reporting speed, and translating raw data "
    "into impactful visual narratives that drive strategy.", body_style))
content.append(Spacer(1, 8))

## 3. Core Skills (Improved: Prioritized highly-demanded tools)
content.append(Paragraph("CORE SKILLS", header_style))
skills = [
    "Programming Languages: Python, R",
    "Data Analysis Tools: **Pandas**, **NumPy**, Matplotlib, Seaborn, ggplot2", 
    "Data Visualization & BI: Dashboards, Reports, Graphs, Charts, **Power BI**", 
    "Statistical Techniques: Hypothesis Testing, Regression, Correlation, ANOVA",
    "Data Handling: Cleaning, Transformation, Feature Engineering, SQL"
]
for s in skills:
    content.append(Paragraph("• " + s, bullet_style))
content.append(Spacer(1, 8))

## 4. Technical Competencies (Improved: Removed "Basic/Introductory")
content.append(Paragraph("TECHNICAL COMPETENCIES", header_style))
competencies = [
    "Database Management: **SQL**, SQLite",
    "Version Control: Git, GitHub",
    "Cloud Platform: AWS (Data Storage and Processing)",
    "Workflow & Environment: Jupyter Notebook, Google Colab, Excel, Kaggle, Notion"
]
for c in competencies:
    content.append(Paragraph("• " + c, bullet_style))
content.append(Spacer(1, 8))

## 5. Professional Experience (Improved: Stronger title, re-phrased bullet points)
content.append(Paragraph("PROFESSIONAL EXPERIENCE", header_style))
content.append(Paragraph("<b>Independent Data Analysis Consultant</b> | Freelance & Academic Projects — Remote (Jan 2023 – Present)", body_style))
experience_points = [
    "Analyzed and interpreted datasets of **10,000+ records** to identify performance trends and **inform strategic recommendations** for client projects.",
    "**Developed and automated** Python scripts that reduced data cleaning and processing time by **over 40%**.", 
    "**Designed and presented** dashboards and visual reports that improved stakeholder data understanding by **30%**.", 
    "Utilized Google Colab and Jupyter Notebook for reproducible, **well-documented workflows and model versioning**.",
    "Collaborated with Kaggle and GitHub communities to share and **validate novel data solutions**."
]
for e in experience_points:
    content.append(Paragraph("• " + e, bullet_style))
content.append(Spacer(1, 8))

## 6. Projects (No Change - Already strong)
content.append(Paragraph("PROJECTS", header_style))
projects = [
    "<b>Sales Performance Dashboard:</b> Built an interactive dashboard using Python (Matplotlib & Seaborn) to visualize sales metrics, improving reporting time by 25%.",
    "<b>Predictive Model for Customer Retention:</b> Developed a logistic regression model that improved accuracy by 15% through feature engineering.",
    "<b>COVID-19 Data Analysis (R):</b> Visualized global COVID-19 trends using ggplot2; delivered insights on infection rates and recovery."
]
for p in projects:
    content.append(Paragraph("• " + p, bullet_style))
content.append(Spacer(1, 8))

## 7. Certifications (Moved higher for impact)
content.append(Paragraph("CERTIFICATIONS", header_style))
certs = [
    "Google Data Analytics Professional Certificate – Coursera", 
    "Data Analysis with Python – Coursera / IBM",
    "Introduction to R for Data Science – DataCamp / Kaggle"
]
for cert in certs:
    content.append(Paragraph("• " + cert, bullet_style))
content.append(Spacer(1, 8))

## 8. Education
content.append(Paragraph("EDUCATION", header_style))
content.append(Paragraph("<b>University of Uyo, Uyo</b>", body_style))
content.append(Paragraph("• Master of Engineering (M.Eng.) in Agricultural Engineering – 2024", body_style))
content.append(Paragraph("• Bachelor of Engineering (B.Eng.) in Agricultural Engineering – 2019", body_style))
content.append(Spacer(1, 8))

## 9. Soft Skills & Attributes (Combined and streamlined)
content.append(Paragraph("SOFT SKILLS & PROFESSIONAL ATTRIBUTES", header_style))
attributes = "Critical Thinking • Problem Solving • Communication • Attention to Detail • Collaboration"
content.append(Paragraph(attributes, body_style))
content.append(Spacer(1, 8))

# Build the document
doc.build(content)

print(f"✅ Optimized and ATS-friendly CV generated successfully: {pdf_file}")

