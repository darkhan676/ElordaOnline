from io import BytesIO
import tempfile
from reportlab.lib.pagesizes import landscape
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from qrcode import QRCode
from random import randint
from django.http import StreamingHttpResponse
import os

"""
        Формат входных параметров:

        data = {
            name: ФИО,
            course: курс/тема,
            course_url:  ссылка на подтверждение (для QR кода),
        }
"""


template_path = os.path.join('certificate_template.png')
font_path = "/usr/share/fonts/truetype/msttcorefonts/arialbd.ttf"

pdfmetrics.registerFont(TTFont('Arial-Bold', font_path))

def create_certificate(data: dict) -> str:
    random_number = f"CA{randint(9999, 99999)}"
    text = "Свидетельствует о прохождении курса повышения квалификации,"
    text2 = f"по теме «{data['course']}» в объеме 72 часа."
    # pdf = canvas.Canvas(f"{data['name']}.pdf", pagesize=landscape((1280, 986)))
    # pdf.drawImage(template_path, 0, 0, width=1280, height=986)

    # pdf.setFont("Arial-Bold", 32)
    # pdf.drawString(520, 650, data["name"])

    # pdf.setFontSize(22)
    # pdf.drawString(270, 550, text)  
    # pdf.drawString(450, 525, text2) 
    # pdf.setFontSize(19)
    # pdf.drawString(1080, 100, "19.05.2023")
    # pdf.drawString(1115, 70, random_number) 
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=landscape((1280, 986)))
    pdf.drawImage(template_path, 0, 0, width=1280, height=986)
    pdf.setFont("Arial-Bold", 32)
    pdf.drawString(520, 650, data["name"])
    pdf.setFontSize(22)
    pdf.drawString(270, 550, text)  
    pdf.drawString(450, 525, text2) 
    pdf.setFontSize(19)
    pdf.drawString(1080, 100, "19.05.2023")
    pdf.drawString(1115, 70, random_number)
    
    
    qr = QRCode(version=1, box_size=10, border=2)
    qr.add_data("https://eao.kz/validation.php")
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    with tempfile.NamedTemporaryFile(delete=False) as f:
        img.save(f, format="PNG")
        qr_filename = f.name
    pdf.drawImage(qr_filename, 220, 45, width=160, height=160)

    os.unlink(qr_filename)

    pdf.save() 
    buffer.seek(0)
    # print(pdf)
    return buffer;
    
data = {
    "name": "Админ Админов",
    "course": "Django 4",
    "course_url": "Data from course"
}

create_certificate(data)