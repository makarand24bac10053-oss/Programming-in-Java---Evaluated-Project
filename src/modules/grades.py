"""
grades.py
---------
Functional Module 3: Grades / marks recording and retrieval.
"""

from src.database import get_connection
from src.utils.logger import get_logger
from src.utils.validators import validate_non_empty, validate_marks
from src.modules.student_management import get_student
from src.modules.subject_management import get_subject

logger = get_logger(__name__)


def record_marks(student_id: int, subject_id: int, assessment_name: str, marks_obtained):
    get_student(student_id)
    subject = get_subject(subject_id)
    assessment_name = validate_non_empty(assessment_name, "Assessment name")
    marks_obtained = validate_marks(marks_obtained, subject["max_marks"])

    conn = get_connection()
    try:
        with conn:
            conn.execute(
                """INSERT INTO marks (student_id, subject_id, assessment_name, marks_obtained)
                   VALUES (?, ?, ?, ?)""",
                (student_id, subject_id, assessment_name, marks_obtained),
            )
        logger.info(
            "Marks recorded: student=%s subject=%s assessment=%s marks=%s",
            student_id, subject_id, assessment_name, marks_obtained,
        )
    finally:
        conn.close()


def get_marks_for_student(student_id: int):
    get_student(student_id)
    conn = get_connection()
    try:
        rows = conn.execute(
            """SELECT m.assessment_name, m.marks_obtained, s.subject_name, s.max_marks
               FROM marks m JOIN subjects s ON m.subject_id = s.subject_id
               WHERE m.student_id = ? ORDER BY s.subject_name""",
            (student_id,),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_average_percentage(student_id: int) -> float:
    """Average percentage across all recorded assessments for a student."""
    records = get_marks_for_student(student_id)
    if not records:
        return 0.0
    percentages = [
        (r["marks_obtained"] / r["max_marks"]) * 100 for r in records if r["max_marks"]
    ]
    return round(sum(percentages) / len(percentages), 2) if percentages else 0.0
