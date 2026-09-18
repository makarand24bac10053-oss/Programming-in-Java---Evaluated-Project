"""
student_management.py
----------------------
Functional Module 1: Student Management (CRUD operations).
"""

import sqlite3
from src.database import get_connection
from src.utils.logger import get_logger
from src.utils.validators import validate_non_empty, validate_email, validate_year

logger = get_logger(__name__)


def add_student(roll_number: str, name: str, email: str, enrolled_year) -> int:
    roll_number = validate_non_empty(roll_number, "Roll number")
    name = validate_non_empty(name, "Name")
    email = validate_email(email or "")
    enrolled_year = validate_year(enrolled_year)

    conn = get_connection()
    try:
        with conn:
            cur = conn.execute(
                "INSERT INTO students (roll_number, name, email, enrolled_year) "
                "VALUES (?, ?, ?, ?)",
                (roll_number, name, email, enrolled_year),
            )
        logger.info("Student added: %s (%s)", name, roll_number)
        return cur.lastrowid
    except sqlite3.IntegrityError:
        raise ValueError(f"A student with roll number '{roll_number}' already exists.")
    finally:
        conn.close()


def list_students():
    conn = get_connection()
    try:
        rows = conn.execute("SELECT * FROM students ORDER BY name").fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_student(student_id: int):
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM students WHERE student_id = ?", (student_id,)
        ).fetchone()
        if not row:
            raise ValueError(f"No student found with ID {student_id}.")
        return dict(row)
    finally:
        conn.close()


def find_student_by_roll(roll_number: str):
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM students WHERE roll_number = ?", (roll_number,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def update_student(student_id: int, name=None, email=None, enrolled_year=None):
    student = get_student(student_id)  # raises if missing

    new_name = validate_non_empty(name, "Name") if name else student["name"]
    new_email = validate_email(email) if email is not None else student["email"]
    new_year = validate_year(enrolled_year) if enrolled_year else student["enrolled_year"]

    conn = get_connection()
    try:
        with conn:
            conn.execute(
                "UPDATE students SET name=?, email=?, enrolled_year=? WHERE student_id=?",
                (new_name, new_email, new_year, student_id),
            )
        logger.info("Student updated: ID %s", student_id)
    finally:
        conn.close()


def delete_student(student_id: int):
    get_student(student_id)  # raises if missing
    conn = get_connection()
    try:
        with conn:
            conn.execute("DELETE FROM students WHERE student_id=?", (student_id,))
        logger.info("Student deleted: ID %s", student_id)
    finally:
        conn.close()
