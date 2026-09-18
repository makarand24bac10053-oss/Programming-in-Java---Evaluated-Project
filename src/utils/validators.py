"""
validators.py
-------------
Reusable input validation helpers (non-functional requirement:
Error handling / Reliability). Each function raises ValueError with
a human-readable message on invalid input, which calling modules
catch and display to the user instead of crashing.
"""

import re

EMAIL_REGEX = re.compile(r"^[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}$")


def validate_non_empty(value: str, field_name: str) -> str:
    if value is None or not value.strip():
        raise ValueError(f"{field_name} cannot be empty.")
    return value.strip()


def validate_email(email: str) -> str:
    email = email.strip()
    if email and not EMAIL_REGEX.match(email):
        raise ValueError(f"'{email}' is not a valid email address.")
    return email


def validate_year(year, min_year: int = 2000, max_year: int = 2100) -> int:
    try:
        year = int(year)
    except (TypeError, ValueError):
        raise ValueError("Enrolled year must be a number.")
    if not (min_year <= year <= max_year):
        raise ValueError(f"Enrolled year must be between {min_year} and {max_year}.")
    return year


def validate_marks(marks, max_marks: float) -> float:
    try:
        marks = float(marks)
    except (TypeError, ValueError):
        raise ValueError("Marks must be numeric.")
    if not (0 <= marks <= max_marks):
        raise ValueError(f"Marks must be between 0 and {max_marks}.")
    return marks


def validate_status(status: str) -> str:
    status = status.strip().lower()
    if status not in ("present", "absent"):
        raise ValueError("Attendance status must be 'present' or 'absent'.")
    return status
