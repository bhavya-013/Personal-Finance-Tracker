from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph
)

from reportlab.lib.styles import getSampleStyleSheet

def generate_report(
        income,
        expense,
        balance):

    pdf = SimpleDocTemplate(
        "exports/report.pdf"
    )

    styles = getSampleStyleSheet()

    content = [

        Paragraph(
            "Personal Finance Report",
            styles["Title"]
        ),

        Paragraph(
            f"Income: ₹{income}",
            styles["Normal"]
        ),

        Paragraph(
            f"Expense: ₹{expense}",
            styles["Normal"]
        ),

        Paragraph(
            f"Balance: ₹{balance}",
            styles["Normal"]
        )

    ]

    pdf.build(content)