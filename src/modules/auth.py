"""
auth.py
-------
Handles user registration and login (Security non-functional
requirement). Passwords are never stored in plain text - they are
salted and hashed using Python's built-in hashlib.pbkdf2_hmac.
"""

import hashlib
import os
import sqlite3
from src.database import get_connection
from src.utils.logger import get_logger
from src.utils.validators import validate_non_empty

logger = get_logger(__name__)


def _hash_password(password: str, salt: bytes = None) -> str:
    """Return 'salt$hash' hex string using PBKDF2-HMAC-SHA256."""
    if salt is None:
        salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000)
    return f"{salt.hex()}${digest.hex()}"


def _verify_password(password: str, stored: str) -> bool:
    try:
        salt_hex, _ = stored.split("$")
        salt = bytes.fromhex(salt_hex)
    except (ValueError, AttributeError):
        return False
    return _hash_password(password, salt) == stored


def register_user(username: str, password: str, role: str) -> bool:
    username = validate_non_empty(username, "Username")
    password = validate_non_empty(password, "Password")
    if role not in ("admin", "teacher"):
        raise ValueError("Role must be 'admin' or 'teacher'.")
    if len(password) < 6:
        raise ValueError("Password must be at least 6 characters long.")

    conn = get_connection()
    try:
        with conn:
            conn.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                (username, _hash_password(password), role),
            )
        logger.info("User registered: %s (%s)", username, role)
        return True
    except sqlite3.IntegrityError:
        raise ValueError(f"Username '{username}' already exists.")
    finally:
        conn.close()


def login_user(username: str, password: str):
    """Return the user row (as dict) if credentials are valid, else None."""
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        if row and _verify_password(password, row["password_hash"]):
            logger.info("Login success: %s", username)
            return dict(row)
        logger.warning("Login failed for username: %s", username)
        return None
    finally:
        conn.close()


def has_any_user() -> bool:
    conn = get_connection()
    try:
        count = conn.execute("SELECT COUNT(*) AS c FROM users").fetchone()["c"]
        return count > 0
    finally:
        conn.close()
