
# ============================================================
#   PDF REPORT GENERATOR
#   Generates a downloadable patient summary PDF
#   using reportlab — no external dependencies
# ============================================================

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.colors import HexColor
from datetime import datetime
import io

# ── Brand Colors ─────────────────────────────────────────────
RED      = HexColor("#C0392B")
DARK_RED = HexColor("#8E1A1A")
DARK_BG  = HexColor("#1a1a2e")
GREEN    = HexColor("#27AE60")
ORANGE   = HexColor("#E67E22")
YELLOW   = HexColor("#F39C12")
BLUE     = HexColor("#2980B9")
GREY     = HexColor("#7F8C8D")
LIGHT_GREY = HexColor("#ECF0F1")
WHITE    = colors.white
BLACK    = colors.black


def status_color(status):
    if "Critical" in status: return HexColor("#E74C3C")
    if "High" in status:     return HexColor("#E67E22")
    if "Low" in status:      return HexColor("#E74C3C")
    if "Borderline" in status: return HexColor("#F39C12")
    return GREEN


def generate_pdf_report(patient_info, results, output_path=None):
    """
    Generate a complete blood report summary PDF.
    Returns bytes if output_path is None, else saves to file.
    """
    buffer = io.BytesIO() if output_path is None else output_path
    
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=15*mm,
        leftMargin=15*mm,
        topMargin=15*mm,
        bottomMargin=15*mm,
    )

    styles = getSampleStyleSheet()
    story  = []

    # ── Custom Styles ─────────────────────────────────────────
    title_style = ParagraphStyle(
        "Title", parent=styles["Normal"],
        fontSize=22, textColor=WHITE,
        fontName="Helvetica-Bold",
        alignment=TA_CENTER, spaceAfter=4,
    )
    subtitle_style = ParagraphStyle(
        "Subtitle", parent=styles["Normal"],
        fontSize=10, textColor=HexColor("#BDC3C7"),
        alignment=TA_CENTER, spaceAfter=2,
    )
    section_heading = ParagraphStyle(
        "SectionHeading", parent=styles["Normal"],
        fontSize=13, textColor=WHITE,
        fontName="Helvetica-Bold",
        backColor=RED,
        borderPad=6, leftIndent=0,
        spaceBefore=10, spaceAfter=6,
    )
    body_style = ParagraphStyle(
        "Body", parent=styles["Normal"],
        fontSize=9, textColor=HexColor("#2C3E50"),
        spaceAfter=4, leading=14,
    )
    small_style = ParagraphStyle(
        "Small", parent=styles["Normal"],
        fontSize=8, textColor=GREY,
        spaceAfter=2,
    )
    bold_style = ParagraphStyle(
        "Bold", parent=styles["Normal"],
        fontSize=9, textColor=BLACK,
        fontName="Helvetica-Bold",
    )
    disclaimer_style = ParagraphStyle(
        "Disclaimer", parent=styles["Normal"],
        fontSize=7.5, textColor=HexColor("#7F8C8D"),
        alignment=TA_CENTER, spaceAfter=2,
        borderColor=HexColor("#E74C3C"),
        borderWidth=0.5, borderPad=6,
        backColor=HexColor("#FDEDEC"),
    )

    # ══════════════════════════════════════════════════════════
    #  HEADER BANNER
    # ══════════════════════════════════════════════════════════
    header_data = [[
        Paragraph("🩸 Smart Blood Report Analyzer", title_style),
    ]]
    header_table = Table(header_data, colWidths=[180*mm])
    header_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), DARK_BG),
        ("TOPPADDING",    (0,0), (-1,-1), 12),
        ("BOTTOMPADDING", (0,0), (-1,-1), 12),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
        ("RIGHTPADDING",  (0,0), (-1,-1), 10),
        ("ROUNDEDCORNERS", [8]),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 4*mm))

    sub = Paragraph("AI-Powered CBC Blood Report Analysis Summary", subtitle_style)
    story.append(sub)
    story.append(Spacer(1, 2*mm))
    story.append(HRFlowable(width="100%", thickness=1, color=RED))
    story.append(Spacer(1, 4*mm))

    # ══════════════════════════════════════════════════════════
    #  PATIENT INFO
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph("  PATIENT INFORMATION", section_heading))

    name   = patient_info.get("name", "Unknown")
    age    = patient_info.get("age", "N/A")
    gender = patient_info.get("gender", "N/A")
    date   = datetime.now().strftime("%d %B %Y, %I:%M %p")

    pat_data = [
        [
            Paragraph(f"<b>Patient Name:</b>  {name}", body_style),
            Paragraph(f"<b>Age:</b>  {age} Years", body_style),
        ],
        [
            Paragraph(f"<b>Gender:</b>  {gender}", body_style),
            Paragraph(f"<b>Report Date:</b>  {date}", body_style),
        ],
        [
            Paragraph("<b>Test:</b>  Complete Blood Count (CBC)", body_style),
            Paragraph("<b>Analysis:</b>  AI + Random Forest ML Model", body_style),
        ],
    ]
    pat_table = Table(pat_data, colWidths=[90*mm, 90*mm])
    pat_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), LIGHT_GREY),
        ("GRID",       (0,0), (-1,-1), 0.3, HexColor("#BDC3C7")),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
    ]))
    story.append(pat_table)
    story.append(Spacer(1, 4*mm))

    # ══════════════════════════════════════════════════════════
    #  HEALTH SCORE
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph("  HEALTH SCORE", section_heading))

    score = results["health_score"]
    label = results["score_label"]
    advice = results["score_advice"]

    if score >= 90:   sc = GREEN
    elif score >= 75: sc = HexColor("#27AE60")
    elif score >= 60: sc = ORANGE
    elif score >= 40: sc = HexColor("#E67E22")
    else:             sc = RED

    score_style = ParagraphStyle(
        "Score", parent=styles["Normal"],
        fontSize=36, textColor=sc,
        fontName="Helvetica-Bold",
        alignment=TA_CENTER,
    )
    score_label_style = ParagraphStyle(
        "ScoreLabel", parent=styles["Normal"],
        fontSize=13, textColor=sc,
        fontName="Helvetica-Bold",
        alignment=TA_CENTER,
    )
    score_advice_style = ParagraphStyle(
        "ScoreAdvice", parent=styles["Normal"],
        fontSize=9, textColor=GREY,
        alignment=TA_CENTER,
    )

    score_data = [[
        Paragraph(f"{score}", score_style),
        Table([
            [Paragraph(f"{label}", score_label_style)],
            [Paragraph(f"{advice}", score_advice_style)],
            [Paragraph(
                f"Normal: {len([a for a in results['abnormalities'] if a['status']=='Normal'])}  |  "
                f"Abnormal: {len([a for a in results['abnormalities'] if a['status']!='Normal'])}  |  "
                f"Conditions: {len(results['diseases'])}",
                small_style
            )],
        ], colWidths=[130*mm]),
    ]]
    score_table = Table(score_data, colWidths=[40*mm, 140*mm])
    score_table.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), LIGHT_GREY),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("LINEAFTER",     (0,0), (0,-1), 1.5, sc),
    ]))
    story.append(score_table)
    story.append(Spacer(1, 4*mm))

    # ══════════════════════════════════════════════════════════
    #  CBC PARAMETERS TABLE
    # ══════════════════════════════════════════════════════════
    story.append(Paragraph("  CBC PARAMETER DETAILS", section_heading))

    param_header = [
        Paragraph("<b>Parameter</b>", bold_style),
        Paragraph("<b>Result</b>", bold_style),
        Paragraph("<b>Reference Range</b>", bold_style),
        Paragraph("<b>Unit</b>", bold_style),
        Paragraph("<b>Status</b>", bold_style),
    ]
    param_rows = [param_header]

    for item in results["abnormalities"]:
        sc_color = status_color(item["status"])
        status_p = ParagraphStyle(
            "Status", parent=styles["Normal"],
            fontSize=8.5, textColor=sc_color,
            fontName="Helvetica-Bold",
        )
        value_p = ParagraphStyle(
            "Value", parent=styles["Normal"],
            fontSize=9, textColor=sc_color,
            fontName="Helvetica-Bold",
        )
        param_rows.append([
            Paragraph(item["parameter"], body_style),
            Paragraph(str(item["value"]), value_p),
            Paragraph(f"{item['low']} – {item['high']}", small_style),
            Paragraph(item["unit"], small_style),
            Paragraph(item["status"], status_p),
        ])

    param_table = Table(param_rows, colWidths=[42*mm, 28*mm, 42*mm, 22*mm, 46*mm])
    param_table.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0), RED),
        ("TEXTCOLOR",     (0,0), (-1,0), WHITE),
        ("GRID",          (0,0), (-1,-1), 0.3, HexColor("#BDC3C7")),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, LIGHT_GREY]),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]))
    story.append(param_table)
    story.append(Spacer(1, 4*mm))

    # ══════════════════════════════════════════════════════════
    #  DISEASE PREDICTIONS
    # ══════════════════════════════════════════════════════════
    if results["diseases"]:
        story.append(Paragraph("  PREDICTED CONDITIONS & HEALTH ADVICE", section_heading))

        for disease in results["diseases"]:
            conf_color = RED if disease["confidence"] >= 70 else ORANGE if disease["confidence"] >= 40 else YELLOW

            # Disease header
            d_header_style = ParagraphStyle(
                "DHead", parent=styles["Normal"],
                fontSize=11, textColor=WHITE,
                fontName="Helvetica-Bold",
                backColor=conf_color,
                borderPad=5,
            )
            conf_style = ParagraphStyle(
                "Conf", parent=styles["Normal"],
                fontSize=9, textColor=WHITE,
                backColor=conf_color,
                alignment=TA_RIGHT, borderPad=5,
            )
            d_head_data = [[
                Paragraph(f"  {disease['name']}", d_header_style),
                Paragraph(f"Confidence: {disease['confidence']}%  ", conf_style),
            ]]
            d_head_table = Table(d_head_data, colWidths=[130*mm, 50*mm])
            d_head_table.setStyle(TableStyle([
                ("BACKGROUND",    (0,0), (-1,-1), conf_color),
                ("TOPPADDING",    (0,0), (-1,-1), 6),
                ("BOTTOMPADDING", (0,0), (-1,-1), 6),
                ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
            ]))
            story.append(d_head_table)

            # Description + Urgency
            desc_data = [
                [Paragraph(f"<b>What is it?</b>  {disease['description']}", body_style)],
                [Paragraph(f"<b>When to act:</b>  {disease['urgency']}  |  <b>Consult:</b>  {disease['doctor']}", body_style)],
            ]
            desc_table = Table(desc_data, colWidths=[180*mm])
            desc_table.setStyle(TableStyle([
                ("BACKGROUND",    (0,0), (-1,-1), HexColor("#FDFEFE")),
                ("GRID",          (0,0), (-1,-1), 0.3, HexColor("#D5D8DC")),
                ("TOPPADDING",    (0,0), (-1,-1), 5),
                ("BOTTOMPADDING", (0,0), (-1,-1), 5),
                ("LEFTPADDING",   (0,0), (-1,-1), 8),
            ]))
            story.append(desc_table)

            # Food + Medicine in 2 columns
            eat_text   = "<b>Foods to EAT:</b><br/>" + "<br/>".join([f"✓ {f}" for f in disease["foods_eat"][:5]])
            avoid_text = "<b>Foods to AVOID:</b><br/>" + "<br/>".join([f"✗ {f}" for f in disease["foods_avoid"][:4]])
            med_text   = "<b>Medications (consult doctor):</b><br/>" + "<br/>".join([f"• {m}" for m in disease["medicines"][:4]])

            food_eat_style = ParagraphStyle("FoodEat", parent=styles["Normal"],
                fontSize=8, textColor=HexColor("#1E8449"), leading=13)
            food_avoid_style = ParagraphStyle("FoodAvoid", parent=styles["Normal"],
                fontSize=8, textColor=HexColor("#C0392B"), leading=13)
            med_style_p = ParagraphStyle("Med", parent=styles["Normal"],
                fontSize=8, textColor=HexColor("#1A5276"), leading=13)

            advice_data = [[
                Paragraph(eat_text, food_eat_style),
                Paragraph(avoid_text, food_avoid_style),
                Paragraph(med_text, med_style_p),
            ]]
            advice_table = Table(advice_data, colWidths=[60*mm, 60*mm, 60*mm])
            advice_table.setStyle(TableStyle([
                ("BACKGROUND",    (0,0), (0,-1), HexColor("#EAFAF1")),
                ("BACKGROUND",    (1,0), (1,-1), HexColor("#FDEDEC")),
                ("BACKGROUND",    (2,0), (2,-1), HexColor("#EBF5FB")),
                ("GRID",          (0,0), (-1,-1), 0.3, HexColor("#D5D8DC")),
                ("TOPPADDING",    (0,0), (-1,-1), 6),
                ("BOTTOMPADDING", (0,0), (-1,-1), 6),
                ("LEFTPADDING",   (0,0), (-1,-1), 6),
                ("VALIGN",        (0,0), (-1,-1), "TOP"),
            ]))
            story.append(advice_table)
            story.append(Spacer(1, 3*mm))

    # ══════════════════════════════════════════════════════════
    #  DISCLAIMER
    # ══════════════════════════════════════════════════════════
    story.append(Spacer(1, 4*mm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=RED))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(
        "⚠️  MEDICAL DISCLAIMER: This report is generated by an AI system for EDUCATIONAL PURPOSES ONLY. "
        "It does NOT constitute a medical diagnosis or replace professional medical advice. "
        "Always consult a qualified and certified doctor for proper diagnosis and treatment. "
        "In case of emergency in India, call 108.",
        disclaimer_style
    ))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(
        f"Generated by Smart Blood Report Analyzer  |  {date}  |  NLP B.Tech Project",
        ParagraphStyle("Footer", parent=styles["Normal"],
            fontSize=7, textColor=GREY, alignment=TA_CENTER)
    ))

    doc.build(story)

    if output_path is None:
        return buffer.getvalue()
