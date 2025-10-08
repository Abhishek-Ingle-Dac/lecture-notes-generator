from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib import colors

def export_pdf(notes: list, quiz: list, filename="lecture_notes.pdf"):
    """
    Export notes and quiz into a clean, formatted PDF file.
    Supports subheadings (marked by **text**) and structured quiz layout.
    """

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    # -------------------- Custom Styles --------------------
    heading1 = ParagraphStyle(
        name="Heading1",
        parent=styles["Heading1"],
        fontSize=18,
        leading=22,
        spaceAfter=12
    )

    subheading = ParagraphStyle(
        name="Subheading",
        parent=styles["Heading2"],
        fontSize=14,
        leading=18,
        spaceBefore=8,
        spaceAfter=6,
        textColor=colors.HexColor("#1a237e"),  # dark blue
    )

    normal_style = ParagraphStyle(
        name="NormalStyle",
        parent=styles["Normal"],
        fontSize=12,
        leading=15,
        spaceAfter=4,
    )

    answer_style = ParagraphStyle(
        name="Answer",
        parent=styles["Normal"],
        fontSize=12,
        leading=15,
        textColor=colors.green,
        spaceAfter=10,
    )

    story = []

    # -------------------- Lecture Notes Section --------------------
    story.append(Paragraph("Lecture Notes", heading1))
    story.append(Spacer(1, 12))

    for n in notes:
        n = n.strip()
        if not n:
            continue

        # Detect subheadings between **...**
        if n.startswith("**") and n.endswith("**"):
            clean_heading = n.strip("*").strip()
            story.append(Paragraph(clean_heading, subheading))
        else:
            story.append(Paragraph(f"• {n}", normal_style))

        story.append(Spacer(1, 6))

    # -------------------- Quiz Section --------------------
    story.append(Spacer(1, 20))
    story.append(Paragraph("Quiz", heading1))
    story.append(Spacer(1, 12))

    for q in quiz:
        q = q.strip()
        if not q:
            continue

        if q.lower().startswith("q"):
            story.append(Paragraph(f"<b>{q}</b>", normal_style))
        elif q.lower().startswith("answer"):
            story.append(Paragraph(q, answer_style))
            story.append(Spacer(1, 12))
        else:
            story.append(Paragraph(q, normal_style))

    # Build the PDF
    doc.build(story)
    return filename
