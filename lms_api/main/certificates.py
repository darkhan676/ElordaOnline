import tempfile
from reportlab.lib.pagesizes import landscape
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from qrcode import QRCode
import os

"""
        Формат входных параметров:

        data = {
            name: ФИО,
            course: курс/тема,
            course_url:  ссылка на подтверждение (для QR кода),
            date_of_start: дата начала,
            date_of_end: дата окончания
        }
"""


template_path = "C:\\Users\\artem\\code\\ElordaOnline\\lms_api\\main\\certificate_template.jpg"
font_path = "C:\Windows\Fonts\ARIALBD.ttf"

pdfmetrics.registerFont(TTFont('Arial-Bold', font_path))

def create_certificate(data: dict) -> str:

    pdf = canvas.Canvas(f"{data['name']}.pdf", pagesize=landscape((1280, 986)))
    pdf.drawImage(template_path, 0, 0, width=1280, height=986)

    pdf.setFont("Arial-Bold", 32)
    pdf.drawString(560, 700, data["name"])
    pdf.drawString(560, 650, data["course"])

    pdf.setFontSize(22)
    
    pdf.drawString(495, 545, data["date_of_start"])
    pdf.drawString(120, 505, data["date_of_end"])

    pdf.drawString(785, 470, data["date_of_start"])
    pdf.drawString(935, 470, data["date_of_end"])

    qr = QRCode(version=1, box_size=10, border=2)
    qr.add_data(data["course_url"])
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    
    with tempfile.NamedTemporaryFile(delete=False) as f:
        img.save(f, format="PNG")
        qr_filename = f.name

    try:
        pdf.drawImage(qr_filename, 220, 45, width=160, height=160)
    
        os.unlink(qr_filename)

        pdf.save()
        return f"{os.getcwd()}\\{data['name']}.pdf"
    except Exception as e:
        return None