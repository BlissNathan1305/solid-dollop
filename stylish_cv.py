from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet

# Create the document
doc = SimpleDocTemplate("Samuel_Nathaniel_Data_Analyst_CV.pdf", pagesize=A4,
                        leftMargin=0.7*inch, rightMargin=0.7*inch,
                        topMargin=0.7*inch, bottomMargin=0.7*inch)

styles = getSampleStyleSheet()
title_style = ParagraphStyle("Title", fontSize=20, leading=22, fontName="Helvetica-Bold", textColor=colors.HexColor("#1A5276"), spaceAfter=12)
header_style = ParagraphStyle("Header", fontSize=13, leading=14, fontName="Helvetica-Bold", textColor=colors.HexColor("#154360"), spaceAfter=8, underlineWidth=0.5)
body_style = ParagraphStyle("Body", fontSize=10, leading=14, fontName="Helvetica")
bullet_style = ParagraphStyle("Bullet", fontSize=10, leading=14, fontName="Helvetica", leftIndent=12)

content = []

# Header block
content.append(Paragraph("Samuel Nathaniel", title_style))
content.append(Paragraph("📍 Uyo, Nigeria | ✉️ sambless44@gmail.com", body_style))
content.append(Paragraph("🔗 LinkedIn: <a href='https://www.linkedin.com/in/samuel-n-0522171a0'>linkedin.com/in/samuel-n-0522171a0</a>", body_style))
content.append(Paragraph("💻 GitHub: <a href='https://github.com/BlissNathan1305'>github.com/BlissNathan1305</a>", body_style))
content.append(Spacer(1, 10))

# Blue divider line
table = Table([[" "]], colWidths=[6.3*inch])
table.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#1A5276")), ("BOTTOMPADDING", (0,0), (-1,-1), 1)]))
content.append(table)
content.append(Spacer(1, 12))

# Professional Summary
content.append(Paragraph("PROFESSIONAL SUMMARY", header_style))
content.append(Paragraph(
    "Analytical and detail-oriented <b>Data Analyst</b> with strong experience in leveraging <b>Python</b> and <b>R</b> "
    "to clean, analyze, and visualize data for impactful insights. Adept at using data-driven methods to inform "
    "business strategies, improve operational efficiency, and automate reporting processes. Skilled in developing "
    "dashboards, performing statistical analysis, and delivering measurable outcomes.", body_style))
content.append(Spacer(1, 8))

# Core Skills
content.append(Paragraph("CORE SKILLS", header_style))
skills = [
    "Programming: Python, R",
    "Data Tools: Pandas, NumPy, Matplotlib, Seaborn, ggplot2",
    "Statistical Analysis: Regression, Hypothesis Testing, ANOVA",
    "Data Visualization: Reports, Dashboards, Charts",
    "Data Handling: Cleaning, Transformation, Feature Engineering",
    "Others: Excel, Google Colab, Jupyter Notebook, Kaggle"
]
for s in skills:
    content.append(Paragraph("• " + s, bullet_style))
content.append(Spacer(1, 8))

# Technical Competencies
content.append(Paragraph("TECHNICAL COMPETENCIES", header_style))
tech = [
    "Version Control: Git, GitHub",
    "Database: SQL (basic), SQLite",
    "Cloud: AWS (Data Storage & Processing)",
    "Reporting Tools: Power BI (Introductory Level)",
    "Collaboration: Google Workspace, Slack, Notion"
]
for t in tech:
    content.append(Paragraph("• " + t, bullet_style))
content.append(Spacer(1, 8))

# Experience
content.append(Paragraph("PROFESSIONAL EXPERIENCE", header_style))
content.append(Paragraph("<b>Freelance / Academic Data Analyst</b> — Remote | Jan 2023 – Present", body_style))
experience_points = [
    "Analyzed datasets of 10,000+ records to identify key patterns and optimize reporting accuracy.",
    "Automated data cleaning pipelines in Python, reducing manual effort by 40%.",
    "Developed visual dashboards that improved business reporting turnaround by 25%.",
    "Collaborated in online data communities (Kaggle, GitHub) to refine model accuracy and reproducibility."
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
    "<b>Sales Performance Dashboard:</b> Built interactive sales analytics using Python (Matplotlib & Seaborn) to track KPIs and trends.",
    "<b>Customer Retention Model:</b> Applied logistic regression to predict churn; improved model accuracy by 15%.",
    "<b>COVID-19 Data Analysis (R):</b> Used ggplot2 to visualize global infection trends and policy impacts."
]
for p in projects:
    content.append(Paragraph("• " + p, bullet_style))
content.append(Spacer(1, 8))

# Achievements
content.append(Paragraph("ACHIEVEMENTS", header_style))
achievements = [
    "Top 20% in Kaggle beginner analytics competitions.",
    "Automated recurring data cleaning scripts saving 3+ hours weekly.",
    "Contributed open-source analytics notebooks on GitHub."
]
for a in achievements:
    content.append(Paragraph("• " + a, bullet_style))
content.append(Spacer(1, 8))

# Soft Skills
content.append(Paragraph("SOFT SKILLS", header_style))
content.append(Paragraph("Analytical Thinking • Communication • Team Collaboration • Problem Solving • Adaptability", body_style))
content.append(Spacer(1, 8))

# Interests
content.append(Paragraph("INTERESTS", header_style))
content.append(Paragraph("Data Science • AI • Machine Learning • Business Intelligence • Visualization", body_style))
content.append(Spacer(1, 10))

# Stylish bottom divider
footer_table = Table([[" "]], colWidths=[6.3*inch])
footer_table.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#1A5276")), ("BOTTOMPADDING", (0,0), (-1,-1), 1)]))
content.append(footer_table)

# Build the final PDF
doc.build(content)
print("✅ Stylish CV PDF successfully created: Samuel_Nathaniel_Data_Analyst_CV.pdf")
