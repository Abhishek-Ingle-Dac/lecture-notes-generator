from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT

def export_pdf(notes: list, quiz: list, filename="lecture_notes.pdf"):
    """
    Export notes and quiz into a clean, formatted PDF file.
    """
    # Create the PDF document
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    # Custom styles
    heading_style = ParagraphStyle(
        name="Heading",
        parent=styles["Heading2"],
        alignment=TA_LEFT,
        spaceAfter=8,
        spaceBefore=8,
        fontSize=13,
        leading=16,
    )

    normal_style = styles["Normal"]

    # Story = flow of PDF content
    story = []

    # Add Lecture Notes Section
    story.append(Paragraph("Lecture Notes", styles["Heading1"]))
    story.append(Spacer(1, 12))

    for n in notes:
        n = n.strip()
        if not n:
            continue

        # Detect headings like **Key Topics**
        if n.startswith("**") and n.endswith("**"):
            clean_heading = n.strip("*").strip()
            story.append(Paragraph(clean_heading, heading_style))
        else:
            story.append(Paragraph(f"• {n}", normal_style))

        story.append(Spacer(1, 6))

    # Add Quiz Section
    story.append(Spacer(1, 20))
    story.append(Paragraph("Quiz", styles["Heading1"]))
    story.append(Spacer(1, 12))

    for q in quiz:
        q = q.strip()
        if not q:
            continue

        if q.startswith("- Q:"):
            story.append(Paragraph(q.replace("- Q:", "Q:"), normal_style))
        elif q.startswith("- A:"):
            story.append(Paragraph(q.replace("- A:", "A:"), normal_style))
            story.append(Spacer(1, 12))  # space after each Q/A pair

    # Build the PDF
    doc.build(story)
    return filename
