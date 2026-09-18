"""
analytics.py
------------
Functional Module 4: Reporting & analytics. Combines data from the
attendance and grades modules to compute performance summaries and
flag "at-risk" students - the core value-add of the system beyond
plain CRUD.
"""

from src.modules.student_management import list_students
from src.modules.attendance import get_attendance_percentage
from src.modules.grades import get_average_percentage
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Thresholds are configurable constants rather than magic numbers
ATTENDANCE_RISK_THRESHOLD = 75.0   # below this % => attendance risk
MARKS_RISK_THRESHOLD = 40.0        # below this % => academic risk


def build_student_report(student_id: int) -> dict:
    attendance_pct = get_attendance_percentage(student_id)
    marks_pct = get_average_percentage(student_id)

    risk_flags = []
    if attendance_pct < ATTENDANCE_RISK_THRESHOLD:
        risk_flags.append("Low attendance")
    if marks_pct < MARKS_RISK_THRESHOLD:
        risk_flags.append("Low academic performance")

    return {
        "student_id": student_id,
        "attendance_percentage": attendance_pct,
        "average_marks_percentage": marks_pct,
        "at_risk": bool(risk_flags),
        "risk_reasons": risk_flags,
    }


def class_summary_report() -> list:
    """Return a performance summary for every student, sorted by risk first."""
    students = list_students()
    report = []
    for s in students:
        summary = build_student_report(s["student_id"])
        summary["name"] = s["name"]
        summary["roll_number"] = s["roll_number"]
        report.append(summary)

    report.sort(key=lambda r: (not r["at_risk"], -r["average_marks_percentage"]))
    logger.info("Generated class summary report for %d students", len(report))
    return report


def class_average_marks() -> float:
    students = list_students()
    if not students:
        return 0.0
    values = [get_average_percentage(s["student_id"]) for s in students]
    return round(sum(values) / len(values), 2)
