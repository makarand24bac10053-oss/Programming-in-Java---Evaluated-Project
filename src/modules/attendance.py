"""
attendance.py
-------------
Functional Module 2: Attendance tracking (data input & processing).
"""

import sqlite3
from datetime import datetime
from src.database import get_connection
from src.utils.logger import get_logger
from src.utils.validators import validate_status
from src.modules.student_management import get_student
from src.modules.subject_management import get_subject

logger = get_logger(__name__)


def mark_attendance(student_id: int, subject_id: int, date: str, status: str):
    get_student(student_id)       # validates existence
    get_subject(subject_id)       # validates existence
    status = validate_status(status)

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Date must be in YYYY-MM-DD format.")

    conn = get_connection()
    try:
        with conn:
            conn.execute(
                """INSERT INTO attendance (student_id, subject_id, date, status)
                   VALUES (?, ?, ?, ?)
                   ON CONFLICT(student_id, subject_id, date)
                   DO UPDATE SET status = excluded.status""",
                (student_id, subject_id, date, status),
            )
        logger.info(
            "Attendance recorded: student=%s subject=%s date=%s status=%s",
            student_id, subject_id, date, status,
        )
    finally:
        conn.close()


def get_attendance_percentage(student_id: int, subject_id: int = None) -> float:
    get_student(student_id)
    conn = get_connection()
    try:
        if subject_id:
            rows = conn.execute(
                "SELECT status FROM attendance WHERE student_id=? AND subject_id=?",
                (student_id, subject_id),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT status FROM attendance WHERE student_id=?", (student_id,)
            ).fetchall()

        if not rows:
            return 0.0
        present = sum(1 for r in rows if r["status"] == "present")
        return round((present / len(rows)) * 100, 2)
    finally:
        conn.close()


def get_attendance_records(student_id: int):
    conn = get_connection()
    try:
        rows = conn.execute(
            """SELECT a.date, a.status, s.subject_name
               FROM attendance a JOIN subjects s ON a.subject_id = s.subject_id
               WHERE a.student_id = ? ORDER BY a.date""",
            (student_id,),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()
