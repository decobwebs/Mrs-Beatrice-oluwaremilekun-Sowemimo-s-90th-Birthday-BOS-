from datetime import datetime, timedelta
from models import Guest, GuestType  # Import your models
import io
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as ReportLabImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_guest_statistics():
    regular_type = GuestType.query.filter_by(name='Regular').first()
    vip_type = GuestType.query.filter_by(name='VIP').first()

    regular_count = Guest.query.filter_by(guest_type_id=regular_type.id).count() if regular_type else 0
    vip_count = Guest.query.filter_by(guest_type_id=vip_type.id).count() if vip_type else 0

    now = datetime.utcnow()
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    guests_today = Guest.query.filter(Guest.timestamp >= start_of_day).count()

    start_of_week = now - timedelta(days=now.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    guests_this_week = Guest.query.filter(Guest.timestamp >= start_of_week).count()

    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    guests_this_month = Guest.query.filter(Guest.timestamp >= start_of_month).count()

    registration_trends = []
    labels = []
    for i in range(7):
        day = now - timedelta(days=i)
        start_of_day = day.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = day.replace(hour=23, minute=59, second=59, microsecond=999999)
        count = Guest.query.filter(Guest.timestamp.between(start_of_day, end_of_day)).count()
        registration_trends.append(count)
        labels.append(day.strftime('%Y-%m-%d'))
    registration_trends.reverse()
    labels.reverse()

    return {
        'regular_count': regular_count,
        'vip_count': vip_count,
        'guests_today': guests_today,
        'guests_this_week': guests_this_week,
        'guests_this_month': guests_this_month,
        'registration_trends': registration_trends,
        'labels': labels,
    }

def generate_pdf_report(statistics):
    buffer = io.BytesIO()
    pie_chart_buffer = create_pie_chart(statistics['regular_count'], statistics['vip_count'])
    line_graph_buffer = create_line_graph(statistics['labels'], statistics['registration_trends'])

    pdf = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'Title',
        parent=styles['Title'],
        fontSize=24,
        leading=30,
        textColor=colors.HexColor('#2E7D32'),
        alignment=1
    )
    heading_style = ParagraphStyle(
        'Heading',
        parent=styles['Heading2'],
        fontSize=16,
        leading=20,
        textColor=colors.HexColor('#1565C0'),
        alignment=1
    )
    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontSize=12,
        leading=14,
        textColor=colors.black
    )

    story = []
    event_title = "Mrs. Beatrice Oluwaremilekun Sowemimo’s 90th Birthday Celebration"
    story.append(Paragraph(event_title, title_style))
    story.append(Spacer(1, 20))

    stats = [
        f"<b>Total Regular Guests:</b> {statistics['regular_count']}",
        f"<b>Total VIP Guests:</b> {statistics['vip_count']}",
        f"<b>Guests Registered Today:</b> {statistics['guests_today']}",
        f"<b>Guests Registered This Week:</b> {statistics['guests_this_week']}",
        f"<b>Guests Registered This Month:</b> {statistics['guests_this_month']}",
    ]
    for stat in stats:
        story.append(Paragraph(stat, normal_style))
    story.append(Spacer(1, 20))

    story.append(Paragraph("Guest Type Distribution", heading_style))
    story.append(ReportLabImage(pie_chart_buffer, width=300, height=200))
    story.append(Spacer(1, 20))

    story.append(Paragraph("Registration Trends (Last 7 Days)", heading_style))
    story.append(ReportLabImage(line_graph_buffer, width=300, height=200))

    pdf.build(story)
    buffer.seek(0)
    pie_chart_buffer.close()
    line_graph_buffer.close()
    return buffer

def create_pie_chart(regular_count, vip_count):
    buffer = io.BytesIO()
    plt.figure(figsize=(8, 6))
    plt.pie(
        [regular_count, vip_count],
        labels=['Regular', 'VIP'],
        autopct='%1.1f%%',
        colors=['#4CAF50', '#FF9800'],
        textprops={'fontsize': 12}
    )
    plt.title('Guest Type Distribution', fontsize=16, fontweight='bold')
    plt.axis('equal')
    plt.savefig(buffer, format='png', bbox_inches='tight')
    plt.close()
    buffer.seek(0)
    return buffer

def create_line_graph(labels, registration_trends):
    buffer = io.BytesIO()
    plt.figure(figsize=(10, 6))
    plt.plot(
        labels,
        registration_trends,
        marker='o',
        color='#03A9F4',
        linewidth=2,
        markersize=8
    )
    plt.title('Registration Trends (Last 7 Days)', fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Number of Registrations', fontsize=14)
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    plt.close()
    buffer.seek(0)
    return buffer