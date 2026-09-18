"""
main.py
-------
Command-line interface entry point for the Student Performance
Management & Analytics System. Ties together the auth, student
management, subject management, attendance, grades and analytics
modules into a menu-driven workflow.

Run with:  python -m src.main
"""

import sys
from src.database import initialize_database
from src.modules import auth, student_management as sm, subject_management as subm
from src.modules import attendance as att, grades as gr, analytics as an
from src.utils.logger import get_logger

logger = get_logger(__name__)


def prompt(label):
    return input(f"{label}: ").strip()


def pause():
    input("\nPress Enter to continue...")


# ---------------------------------------------------------------- auth ----
def login_flow():
    print("\n=== Login ===")
    if not auth.has_any_user():
        print("No users exist yet. Let's create the first admin account.")
        username = prompt("New admin username")
        password = prompt("New admin password (min 6 chars)")
        try:
            auth.register_user(username, password, "admin")
            print("Admin account created. Please log in.")
        except ValueError as e:
            print(f"Error: {e}")

    for _ in range(3):
        username = prompt("Username")
        password = prompt("Password")
        user = auth.login_user(username, password)
        if user:
            print(f"\nWelcome, {user['username']} ({user['role']})!")
            return user
        print("Invalid credentials, try again.")
    print("Too many failed attempts. Exiting.")
    sys.exit(1)


# ------------------------------------------------------- student module ---
def student_menu():
    while True:
        print("\n--- Student Management ---")
        print("1. Add student\n2. List students\n3. Update student\n"
              "4. Delete student\n5. Back")
        choice = prompt("Choose")
        try:
            if choice == "1":
                sid = sm.add_student(
                    prompt("Roll number"), prompt("Name"),
                    prompt("Email (optional)"), prompt("Enrolled year"),
                )
                print(f"Student added with ID {sid}.")
            elif choice == "2":
                for s in sm.list_students():
                    print(f"[{s['student_id']}] {s['roll_number']} - {s['name']} "
                          f"({s['enrolled_year']}) {s['email'] or ''}")
            elif choice == "3":
                sid = int(prompt("Student ID to update"))
                sm.update_student(
                    sid,
                    name=prompt("New name (blank=skip)") or None,
                    email=prompt("New email (blank=skip)") or None,
                    enrolled_year=prompt("New enrolled year (blank=skip)") or None,
                )
                print("Student updated.")
            elif choice == "4":
                sid = int(prompt("Student ID to delete"))
                sm.delete_student(sid)
                print("Student deleted.")
            elif choice == "5":
                return
            else:
                print("Invalid choice.")
        except ValueError as e:
            print(f"Error: {e}")
        pause()


# ------------------------------------------------------- subject module ---
def subject_menu():
    while True:
        print("\n--- Subject Management ---")
        print("1. Add subject\n2. List subjects\n3. Back")
        choice = prompt("Choose")
        try:
            if choice == "1":
                subm.add_subject(
                    prompt("Subject code"), prompt("Subject name"),
                    prompt("Max marks (default 100)") or 100,
                )
                print("Subject added.")
            elif choice == "2":
                for s in subm.list_subjects():
                    print(f"[{s['subject_id']}] {s['subject_code']} - "
                          f"{s['subject_name']} (max {s['max_marks']})")
            elif choice == "3":
                return
            else:
                print("Invalid choice.")
        except ValueError as e:
            print(f"Error: {e}")
        pause()


# ---------------------------------------------------- attendance module ---
def attendance_menu():
    while True:
        print("\n--- Attendance ---")
        print("1. Mark attendance\n2. View attendance % for a student\n"
              "3. View attendance records\n4. Back")
        choice = prompt("Choose")
        try:
            if choice == "1":
                att.mark_attendance(
                    int(prompt("Student ID")), int(prompt("Subject ID")),
                    prompt("Date (YYYY-MM-DD)"), prompt("Status (present/absent)"),
                )
                print("Attendance recorded.")
            elif choice == "2":
                sid = int(prompt("Student ID"))
                pct = att.get_attendance_percentage(sid)
                print(f"Overall attendance: {pct}%")
            elif choice == "3":
                sid = int(prompt("Student ID"))
                for r in att.get_attendance_records(sid):
                    print(f"{r['date']} | {r['subject_name']} | {r['status']}")
            elif choice == "4":
                return
            else:
                print("Invalid choice.")
        except ValueError as e:
            print(f"Error: {e}")
        pause()


# -------------------------------------------------------- grades module ---
def grades_menu():
    while True:
        print("\n--- Grades ---")
        print("1. Record marks\n2. View marks for a student\n3. Back")
        choice = prompt("Choose")
        try:
            if choice == "1":
                gr.record_marks(
                    int(prompt("Student ID")), int(prompt("Subject ID")),
                    prompt("Assessment name (e.g. Midterm)"), prompt("Marks obtained"),
                )
                print("Marks recorded.")
            elif choice == "2":
                sid = int(prompt("Student ID"))
                for m in gr.get_marks_for_student(sid):
                    print(f"{m['subject_name']} | {m['assessment_name']} | "
                          f"{m['marks_obtained']}/{m['max_marks']}")
            elif choice == "3":
                return
            else:
                print("Invalid choice.")
        except ValueError as e:
            print(f"Error: {e}")
        pause()


# ----------------------------------------------------- analytics module ---
def analytics_menu():
    while True:
        print("\n--- Analytics & Reports ---")
        print("1. Individual student report\n2. Full class summary\n"
              "3. Class average marks\n4. Back")
        choice = prompt("Choose")
        try:
            if choice == "1":
                sid = int(prompt("Student ID"))
                r = an.build_student_report(sid)
                print(f"\nAttendance: {r['attendance_percentage']}%")
                print(f"Average marks: {r['average_marks_percentage']}%")
                print(f"At risk: {'YES - ' + ', '.join(r['risk_reasons']) if r['at_risk'] else 'No'}")
            elif choice == "2":
                print(f"\n{'Roll':<10}{'Name':<20}{'Attendance%':<14}{'Marks%':<10}{'At Risk'}")
                for r in an.class_summary_report():
                    print(f"{r['roll_number']:<10}{r['name']:<20}"
                          f"{r['attendance_percentage']:<14}{r['average_marks_percentage']:<10}"
                          f"{'YES' if r['at_risk'] else 'No'}")
            elif choice == "3":
                print(f"Class average marks: {an.class_average_marks()}%")
            elif choice == "4":
                return
            else:
                print("Invalid choice.")
        except ValueError as e:
            print(f"Error: {e}")
        pause()


# --------------------------------------------------------------- main -----
def main():
    initialize_database()
    print("=========================================")
    print(" Student Performance Management & Analytics System")
    print("=========================================")
    user = login_flow()

    while True:
        print(f"\n=== Main Menu ({user['role']}) ===")
        print("1. Student Management")
        print("2. Subject Management")
        print("3. Attendance")
        print("4. Grades")
        print("5. Analytics & Reports")
        print("6. Exit")
        choice = prompt("Choose")

        if choice == "1":
            student_menu()
        elif choice == "2":
            subject_menu()
        elif choice == "3":
            attendance_menu()
        elif choice == "4":
            grades_menu()
        elif choice == "5":
            analytics_menu()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting cleanly.")
    except Exception as exc:  # top-level safety net
        logger.exception("Unhandled exception: %s", exc)
        print(f"An unexpected error occurred: {exc}")
