from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from datetime import datetime


def create_report(
    filepath,
    score,
    report_summary,
    weak_topics,
    history=None,
    bookmarks=None,
    study_sessions=None
):

    history = history or []
    bookmarks = bookmarks or []
    study_sessions = study_sessions or []

    styles = getSampleStyleSheet()

    title_style = styles["Title"]

    title_style.alignment = TA_CENTER

    heading_style = styles["Heading2"]

    normal_style = styles["BodyText"]

    document = SimpleDocTemplate(
        filepath,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    content = []

    # ==================================================
    # TITLE
    # ==================================================

    content.append(
        Paragraph(
            "🎓 AI Study Buddy",
            title_style
        )
    )

    content.append(
        Paragraph(
            "Personal Learning Report",
            heading_style
        )
    )

    content.append(
        Spacer(1, 15)
    )

    content.append(
        Paragraph(
            f"Generated on: "
            f"{datetime.now().strftime('%d %B %Y %I:%M %p')}",
            normal_style
        )
    )

    content.append(
        Spacer(1, 20)
    )

    # ==================================================
    # OVERVIEW
    # ==================================================

    content.append(
        Paragraph(
            "📊 Learning Overview",
            heading_style
        )
    )

    overview_data = [
        ["Metric", "Value"],
        [
            "Latest Quiz Score",
            f"{score:.1f}%"
        ],
        [
            "Quiz Attempts",
            str(len(history))
        ],
        [
            "Study Sessions",
            str(len(study_sessions))
        ],
        [
            "Bookmarked Topics",
            str(len(bookmarks))
        ]
    ]

    table = Table(
        overview_data,
        colWidths=[250, 150]
    )

    table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.lightgrey
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                1,
                colors.grey
            ),
            (
                "PADDING",
                (0, 0),
                (-1, -1),
                8
            )
        ])
    )

    content.append(table)

    content.append(
        Spacer(1, 20)
    )

    # ==================================================
    # SUMMARY
    # ==================================================

    content.append(
        Paragraph(
            "📝 Learning Summary",
            heading_style
        )
    )

    content.append(
        Paragraph(
            report_summary,
            normal_style
        )
    )

    content.append(
        Spacer(1, 20)
    )

    # ==================================================
    # WEAK TOPICS
    # ==================================================

    content.append(
        Paragraph(
            "🎯 Weak Concepts",
            heading_style
        )
    )

    if weak_topics:

        for topic in weak_topics:

            content.append(
                Paragraph(
                    f"• {topic}",
                    normal_style
                )
            )

    else:

        content.append(
            Paragraph(
                "No weak concepts detected.",
                normal_style
            )
        )

    content.append(
        Spacer(1, 20)
    )

    # ==================================================
    # QUIZ HISTORY
    # ==================================================

    content.append(
        Paragraph(
            "📈 Quiz History",
            heading_style
        )
    )

    if history:

        quiz_data = [
            [
                "Date",
                "Score",
                "Weak Topics"
            ]
        ]

        for item in history:

            quiz_data.append([
                item.get("date", ""),
                f"{item.get('percentage', 0)}%",
                ", ".join(
                    item.get(
                        "weak_topics",
                        []
                    )
                )
            ])

        quiz_table = Table(
            quiz_data,
            colWidths=[
                130,
                70,
                200
            ]
        )

        quiz_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.grey
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    6
                )
            ])
        )

        content.append(
            quiz_table
        )

    else:

        content.append(
            Paragraph(
                "No quiz history available.",
                normal_style
            )
        )

    content.append(
        Spacer(1, 20)
    )

    # ==================================================
    # BOOKMARKS
    # ==================================================

    content.append(
        Paragraph(
            "📌 Bookmarked Topics",
            heading_style
        )
    )

    if bookmarks:

        for bookmark in bookmarks:

            content.append(
                Paragraph(
                    f"• {bookmark}",
                    normal_style
                )
            )

    else:

        content.append(
            Paragraph(
                "No bookmarks available.",
                normal_style
            )
        )

    content.append(
        Spacer(1, 20)
    )

    # ==================================================
    # STUDY TIME
    # ==================================================

    total_minutes = sum(
        session.get(
            "minutes",
            0
        )
        for session in study_sessions
    )

    hours = total_minutes // 60

    minutes = total_minutes % 60

    content.append(
        Paragraph(
            "⏱️ Study Time",
            heading_style
        )
    )

    content.append(
        Paragraph(
            f"Total study time: "
            f"{hours} hours {minutes} minutes",
            normal_style
        )
    )

    content.append(
        Spacer(1, 20)
    )

    # ==================================================
    # RECOMMENDATION
    # ==================================================

    content.append(
        Paragraph(
            "💡 Recommendation",
            heading_style
        )
    )

    if weak_topics:

        recommendation = (
            "Focus your next study sessions on: "
            + ", ".join(weak_topics)
            + ". Review the concepts, practice questions, "
              "and retake the quiz."
        )

    elif score >= 80:

        recommendation = (
            "Excellent performance. Continue practicing "
            "and try more advanced questions."
        )

    elif score >= 50:

        recommendation = (
            "Your performance is improving. Continue "
            "reviewing your study material and practice "
            "the concepts that caused mistakes."
        )

    else:

        recommendation = (
            "Spend more time reviewing the fundamental "
            "concepts before attempting another quiz."
        )

    content.append(
        Paragraph(
            recommendation,
            normal_style
        )
    )

    document.build(content)

    return filepath