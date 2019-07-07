"""
Reportlab sandbox.
"""
import task_directive as td
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter, landscape

from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfform
from reportlab.lib.colors import magenta, pink, blue, green

import os
from pdf2image import convert_from_path


def basic_list(current_tasks_path):

    tasks = td.sort_tasks(td.load_tasks(current_tasks_path))

    doc = SimpleDocTemplate("directive.pdf", pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=36, bottomMargin=18)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))

    Story = []
    Story.append(Paragraph('''<font size = 16> The Directive <br/><br/></font>''', styles["Center"]))

    logo = "image.png"

    # We really want to scale the image to fit in a box and keep proportions.
    im = Image(logo, 5 * inch, 4 * inch)
    Story.append(im)

    # ptext = '<font size=12>Some text</font>'
    # Story.append(Paragraph(ptext, styles["Normal"]))
    total_time = 0
    for task in tasks:
        total_time += task.complete_time
    ptext = '''<font size = 16> Tasks | ~''' + str(round(total_time,2)) + '''hrs <br/><br/></font>'''
    Story.append(Paragraph(ptext, styles["Normal"]))
    for task in tasks:
        if task.due_time <= 5:
            ptext = '''<font size = 14 color = "Red">O ''' + task.description + ''' | ~''' + str(task.complete_time) + '''hrs''' + '''<br/><br/></font>'''
        elif 5 < task.due_time <= 15:
            ptext = '''<font size = 14 color = "Blue">O ''' + task.description + ''' | ~''' + str(task.complete_time) + '''hrs''' + '''<br/><br/></font>'''
        else:
            ptext = '''<font size = 14>O ''' + task.description + ''' | ~''' + str(task.complete_time) + '''hrs''' + '''<br/><br/></font>'''
        Story.append(Paragraph(ptext, styles["Normal"]))

    doc.build(Story)
    pages = convert_from_path('directive.pdf', 500)
    for page in pages:
        page.save('directive.jpg', 'JPEG')