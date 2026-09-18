"""
test_student_management.py
---------------------------
Unit tests for the student management module. Uses a temporary
SQLite database (via monkeypatching DB_PATH) so tests never touch
real data.
"""

import os
import sys
import unittest
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import src.database as database


class TestStudentManagement(unittest.TestCase):
    def setUp(self):
        # Point the database module at a fresh temp file for isolation
        self.tmp_dir = tempfile.mkdtemp()
        database.DB_PATH = os.path.join(self.tmp_dir, "test.db")
        database.initialize_database()

        # Import after patching DB_PATH so the module uses the patched path
        from src.modules import student_management as sm
        self.sm = sm

    def test_add_and_get_student(self):
        sid = self.sm.add_student("R001", "Alice", "alice@example.com", 2023)
        student = self.sm.get_student(sid)
        self.assertEqual(student["name"], "Alice")
        self.assertEqual(student["roll_number"], "R001")

    def test_duplicate_roll_number_rejected(self):
        self.sm.add_student("R002", "Bob", "bob@example.com", 2023)
        with self.assertRaises(ValueError):
            self.sm.add_student("R002", "Bobby", "bobby@example.com", 2023)

    def test_invalid_email_rejected(self):
        with self.assertRaises(ValueError):
            self.sm.add_student("R003", "Carl", "not-an-email", 2023)

    def test_invalid_year_rejected(self):
        with self.assertRaises(ValueError):
            self.sm.add_student("R004", "Dana", "dana@example.com", 1899)

    def test_update_student(self):
        sid = self.sm.add_student("R005", "Eve", "eve@example.com", 2022)
        self.sm.update_student(sid, name="Eve Updated")
        student = self.sm.get_student(sid)
        self.assertEqual(student["name"], "Eve Updated")

    def test_delete_student(self):
        sid = self.sm.add_student("R006", "Frank", "frank@example.com", 2022)
        self.sm.delete_student(sid)
        with self.assertRaises(ValueError):
            self.sm.get_student(sid)

    def test_get_missing_student_raises(self):
        with self.assertRaises(ValueError):
            self.sm.get_student(9999)


if __name__ == "__main__":
    unittest.main()
