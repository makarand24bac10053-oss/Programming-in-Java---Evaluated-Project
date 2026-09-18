"""
test_grades_and_analytics.py
-----------------------------
Unit tests covering the grades and analytics modules, including the
at-risk detection logic in analytics.py.
"""

import os
import sys
import unittest
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import src.database as database


class TestGradesAndAnalytics(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        database.DB_PATH = os.path.join(self.tmp_dir, "test.db")
        database.initialize_database()

        from src.modules import student_management as sm
        from src.modules import subject_management as subm
        from src.modules import grades as gr
        from src.modules import attendance as att
        from src.modules import analytics as an

        self.sm, self.subm, self.gr, self.att, self.an = sm, subm, gr, att, an

        self.sid = self.sm.add_student("R100", "Test Student", "t@example.com", 2023)
        self.subj_id = self.subm.add_subject("CS101", "Intro to CS", 100)

    def test_record_and_average_marks(self):
        self.gr.record_marks(self.sid, self.subj_id, "Quiz 1", 80)
        self.gr.record_marks(self.sid, self.subj_id, "Quiz 2", 60)
        avg = self.gr.get_average_percentage(self.sid)
        self.assertEqual(avg, 70.0)

    def test_marks_out_of_range_rejected(self):
        with self.assertRaises(ValueError):
            self.gr.record_marks(self.sid, self.subj_id, "Quiz 3", 150)

    def test_at_risk_low_marks(self):
        self.gr.record_marks(self.sid, self.subj_id, "Quiz 1", 20)
        report = self.an.build_student_report(self.sid)
        self.assertTrue(report["at_risk"])
        self.assertIn("Low academic performance", report["risk_reasons"])

    def test_at_risk_low_attendance(self):
        self.att.mark_attendance(self.sid, self.subj_id, "2025-01-01", "absent")
        self.att.mark_attendance(self.sid, self.subj_id, "2025-01-02", "absent")
        self.att.mark_attendance(self.sid, self.subj_id, "2025-01-03", "present")
        report = self.an.build_student_report(self.sid)
        self.assertTrue(report["at_risk"])
        self.assertIn("Low attendance", report["risk_reasons"])

    def test_not_at_risk_when_healthy(self):
        self.gr.record_marks(self.sid, self.subj_id, "Quiz 1", 90)
        for d in ["2025-01-01", "2025-01-02", "2025-01-03", "2025-01-04"]:
            self.att.mark_attendance(self.sid, self.subj_id, d, "present")
        report = self.an.build_student_report(self.sid)
        self.assertFalse(report["at_risk"])


if __name__ == "__main__":
    unittest.main()
