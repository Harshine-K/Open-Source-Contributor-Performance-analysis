from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
import matplotlib.pyplot as plt
import io
from utils import generate_performance_plot, generate_pie_chart

# Your generate_performance_plot function should remain the same
def generate_pdf_report(df, filename='Contributor_Performance_Report.pdf'):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    title = Paragraph("Open-Source Contributor Performance Analysis Report", styles['Title'])
    elements.append(title)
    elements.append(Paragraph("<br />", styles['Normal']))

    # Summary Statistics
    summary_stats = f"""
    <b>Total Contributors:</b> {len(df)}<br />
    <b>Top Contributor:</b> {df.loc[df['performance_score'].idxmax()]['login']}<br />
    <b>Average Performance Score:</b> {df['performance_score'].mean():.2f}<br />
    """
    elements.append(Paragraph(summary_stats, styles['Normal']))

    # Performance Plot
    plot_buf = generate_performance_plot(df)  # Assuming this returns a buffer
    elements.append(Image(plot_buf, width=500, height=300))

    elements.append(Paragraph("Top 10 Contributor Performance Breakdown", styles['Normal']))
    plot_buf1 = generate_pie_chart(df)  # Assuming this returns a buffer
    elements.append(Image(plot_buf1, width=500, height=300))

    # Detailed Contributor Performance
    elements.append(Paragraph("<br />Detailed Contributor Performance:", styles['Heading2']))
    table_data = [['Login', 'Contributions', 'Commits', 'Pull Requests', 'Issues', 'Performance Score']]
    for index, row in df.head(100).iterrows():
        table_data.append([row['login'], row['contributions'], row['commits'], row['pull_requests'], row['issues'], row['performance_score']])

    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)

    doc.build(elements)

    return filename