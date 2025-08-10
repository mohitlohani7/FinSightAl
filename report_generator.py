from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def make_simple_pdf_report(title: str, content: str) -> bytes:
    """
    Create a simple PDF report in memory.
    
    Args:
        title (str): Title of the PDF
        content (str): Main body text

    Returns:
        bytes: PDF file bytes
    """
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawString(72, 750, title)

    # Content
    c.setFont("Helvetica", 12)
    y = 720
    for line in content.splitlines():
        c.drawString(72, y, line)
        y -= 14
        if y < 72:  # new page if space runs out
            c.showPage()
            y = 750

    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer.getvalue()
