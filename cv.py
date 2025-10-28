from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib.styles import ParagraphStyle

# Output file
pdf_file = "Samuel_Nathaniel_Data_Analyst_CV.pdf"

# Create PDF doc
doc = SimpleDocTemplate(pdf_file, pagesize=A4,
                        leftMargin=0.8*inch, rightMargin=0.8*inch,
                        topMargin=0.8*inch, bottomMargin=0.8*inch)

styles = getSampleStyleSheet()

# Custom styles
title_style = ParagraphStyle('Title', fontName='Helvetica-Bold', fontSize=18, spaceAfter=10)
header_style = ParagraphStyle('Header', fontName='Helvetica-Bold', fontSize=12, textColor=colors.HexColor("#1A5276"), spaceAfter=6)
body_style = ParagraphStyle('Body', fontName='Helvetica', fontSize=10, leading=14)
bullet_style = ParagraphStyle('Bullet', fontName='Helvetica', fontSize=10, leading=14, leftIndent=12)

# Content list for the PDF
content = []

# Header / Name Section
content.append(Paragraph("<b>Samuel Nathaniel</b>", title_style))
content.append(Paragraph("Uyo, Nigeria | sambless44@gmail.com", body_style))
content.append(Paragraph("LinkedIn: <a href='https://www.linkedin.com/in/samuel-n-0522171a0'>linkedin.com/in/samuel-n-0522171a0</a>", body_style))
content.append(Paragraph("GitHub: <a href='https://github.com/BlissNathan1305'>github.com/BlissNathan1305</a>", body_style))
content.append(Spacer(1, 12))

# Professional Summary
content.append(Paragraph("PROFESSIONAL SUMMARY", header_style))
content.append(Paragraph(
    "Analytical and detail-oriented <b>Data Analyst</b> with a strong foundation in data wrangling, "
    "visualization, and statistical modeling. Experienced in extracting insights from complex datasets "
    "using <b>Python</b> and <b>R</b>, and in presenting actionable findings to support data-driven decisions. "
    "Proven track record of automating workflows, improving reporting speed, and translating raw data "
    "into impactful visual narratives that drive strategy.", body_style))
content.append(Spacer(1, 8))

# Core Skills
content.append(Paragraph("CORE SKILLS", header_style))
skills = [
    "Programming Languages: Python, R",
    "Data Analysis Tools: Pandas, NumPy, ggplot2, Matplotlib, Seaborn",
    "Statistical Techniques: Hypothesis Testing, Regression, Correlation, ANOVA",
    "Data Visualization: Dashboards, Reports, Graphs, Charts",
    "Data Handling: Cleaning, Transformation, Feature Engineering",
    "Others: Jupyter Notebook, Google Colab, Excel, Kaggle"
]
for s in skills:
    content.append(Paragraph("• " + s, bullet_style))
content.append(Spacer(1, 8))

# Technical Competencies
content.append(Paragraph("TECHNICAL COMPETENCIES", header_style))
competencies = [
    "Version Control: Git, GitHub",
    "Database Management: SQL, SQLite (Basic)",
    "Cloud Platform: AWS (Fundamentals – Data Storage and Processing)",
    "Reporting Tools: Power BI (Introductory Level)",
    "Collaboration & Workflow: Google Workspace, Slack, Notion"
]
for c in competencies:
    content.append(Paragraph("• " + c, bullet_style))
content.append(Spacer(1, 8))

# Experience
content.append(Paragraph("PROFESSIONAL EXPERIENCE", header_style))
content.append(Paragraph("<b>Freelance / Academic Data Analyst</b> | Independent Projects — Remote (Jan 2023 – Present)", body_style))
experience_points = [
    "Analyzed and interpreted datasets of 10,000+ records to identify performance trends and correlations.",
    "Automated Python scripts that reduced data cleaning time by over 40%.",
    "Developed dashboards and visual reports that improved stakeholder understanding by 30%.",
    "Utilized Google Colab and Jupyter Notebook for reproducible, well-documented workflows.",
    "Collaborated with Kaggle and GitHub communities to share data solutions."
]
for e in experience_points:
    content.append(Paragraph("• " + e, bullet_style))
content.append(Spacer(1, 8))

# Education
content.append(Paragraph("EDUCATION", header_style))
content.append(Paragraph("<b>University of Uyo, Uyo</b>", body_style))
content.append(Paragraph("• Master of Engineering (M.Eng.) in Agricultural Engineering – 2024", body_style))
content.append(Paragraph("• Bachelor of Engineering (B.Eng.) in Agricultural Engineering – 2019", body_style))
content.append(Spacer(1, 8))

# Certifications
content.append(Paragraph("CERTIFICATIONS", header_style))
certs = [
    "Data Analysis with Python – Coursera / IBM",
    "Introduction to R for Data Science – DataCamp / Kaggle",
    "Google Data Analytics Professional Certificate – Coursera"
]
for cert in certs:
    content.append(Paragraph("• " + cert, bullet_style))
content.append(Spacer(1, 8))

# Projects
content.append(Paragraph("PROJECTS", header_style))
projects = [
    "<b>Sales Performance Dashboard:</b> Built an interactive dashboard using Python (Matplotlib & Seaborn) to visualize sales metrics, improving reporting time by 25%.",
    "<b>Predictive Model for Customer Retention:</b> Developed a logistic regression model that improved accuracy by 15% through feature engineering.",
    "<b>COVID-19 Data Analysis (R):</b> Visualized global COVID-19 trends using ggplot2; delivered insights on infection rates and recovery."
]
for p in projects:
    content.append(Paragraph("• " + p, bullet_style))
content.append(Spacer(1, 8))

# Achievements
content.append(Paragraph("ACHIEVEMENTS", header_style))
achievements = [
    "Ranked in the top 20% of participants in Kaggle beginner competitions.",
    "Automated data-cleaning workflow saving multiple hours weekly.",
    "Published reproducible notebooks and visualizations on GitHub."
]
for a in achievements:
    content.append(Paragraph("• " + a, bullet_style))
content.append(Spacer(1, 8))

# Soft Skills
content.append(Paragraph("SOFT SKILLS", header_style))
soft_skills = "Critical Thinking • Problem Solving • Communication • Attention to Detail • Collaboration"
content.append(Paragraph(soft_skills, body_style))
content.append(Spacer(1, 8))

# Interests
content.append(Paragraph("INTERESTS", header_style))
interests = "Data Science • Artificial Intelligence • Machine Learning • Business Intelligence • Visualization"
content.append(Paragraph(interests, body_style))

# Build the document
doc.build(content)

print(f"✅ Stylish and ATS-friendly CV generated successfully: {pdf_file}")
