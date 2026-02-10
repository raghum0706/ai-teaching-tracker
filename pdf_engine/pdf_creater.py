from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def create_pdf(title, text, path):
    c = canvas.Canvas(path, pagesize=A4)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, title)
    c.setFont("Helvetica", 12)
    y = 770
    for line in text.split("\n"):
        c.drawString(50, y, line)
        y -= 15
    c.save()
