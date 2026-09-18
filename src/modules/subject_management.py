"""
subject_management.py
----------------------
Supporting module for managing subjects/courses that students are
assessed in. Used by both the Attendance and Grades modules.
"""

import sqlite3
from src.database import get_connection
from src.utils.logger import get_logger
from src.utils.validators import validate_non_empty

logger = get_logger(__name__)


def add_subject(subject_code: str, subject_name: str, max_marks: int = 100) -> int:
    subject_code = validate_non_empty(subject_code, "Subject code")
    subject_name = validate_non_empty(subject_name, "Subject name")
    try:
        max_marks = int(max_marks)
        if max_marks <= 0:
            raise ValueError
    except ValueError:
        raise ValueError("Max marks must be a positive whole number.")

    conn = get_connection()
    try:
        with conn:
            cur = conn.execute(
                "INSERT INTO subjects (subject_code, subject_name, max_marks) VALUES (?, ?, ?)",
                (subject_code, subject_name, max_marks),
            )
        logger.info("Subject added: %s", subject_name)
        return cur.lastrowid
    except sqlite3.IntegrityError:
        raise ValueError(f"Subject code '{subject_code}' already exists.")
    finally:
        conn.close()


def list_subjects():
    conn = get_connection()
    try:
        rows = conn.execute("SELECT * FROM subjects ORDER BY subject_name").fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_subject(subject_id: int):
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM subjects WHERE subject_id = ?", (subject_id,)
        ).fetchone()
        if not row:
            raise ValueError(f"No subject found with ID {subject_id}.")
        return dict(row)
    finally:
        conn.close()
