# Student Performance Management & Analytics System

A command-line application for managing student records, attendance,
grades, and generating "at-risk" performance analytics — built for
[COURSE NAME HERE] as part of the flipped-course evaluation project.

## Overview

Teachers and administrators need a simple, reliable way to track
student attendance and marks across subjects, and to quickly identify
students who may need academic support. This system provides a single
CLI tool backed by a local SQLite database to do exactly that, without
requiring any external services or a GUI.

## Features

- **Authentication** — admin/teacher accounts with securely hashed
  passwords (PBKDF2-HMAC-SHA256, salted).
- **Student Management** — add, list, update, and delete student
  records with input validation (email format, enrolment year range,
  unique roll numbers).
- **Subject Management** — define subjects and their maximum marks.
- **Attendance Tracking** — mark present/absent per student per
  subject per date, with duplicate-entry protection (re-marking a
  date updates it instead of creating a duplicate row).
- **Grades Tracking** — record marks per assessment (quiz, midterm,
  etc.) per subject, validated against that subject's max marks.
- **Analytics & Reporting**
  - Per-student report: attendance %, average marks %, and risk flags.
  - Class-wide summary sorted so at-risk students appear first.
  - Class average marks.
- **Logging** — every significant action (registration, login,
  record creation, errors) is logged to `data/app.log` with
  timestamps.
- **Error handling** — all user input is validated; invalid input
  produces a clear message instead of crashing the program.

## Technologies Used

- Python 3.10+ (standard library only — no external dependencies)
- SQLite3 (via `sqlite3` module) for persistent storage
- `hashlib` for password hashing
- `logging` for structured application logs
- `unittest` for automated testing

## Project Structure

```
student-performance-system/
├── src/
│   ├── main.py                  # CLI entry point / menu system
│   ├── database.py              # DB connection + schema
│   ├── modules/
│   │   ├── auth.py              # Registration & login
│   │   ├── student_management.py# Student CRUD
│   │   ├── subject_management.py# Subject CRUD
│   │   ├── attendance.py        # Attendance recording & stats
│   │   ├── grades.py            # Marks recording & stats
│   │   └── analytics.py         # Reports & at-risk detection
│   └── utils/
│       ├── logger.py            # Centralized logging setup
│       └── validators.py        # Input validation helpers
├── tests/
│   ├── test_student_management.py
│   └── test_grades_and_analytics.py
├── data/                        # SQLite DB + logs created at runtime
├── requirements.txt
└── README.md
```

## Setup & Installation

**Prerequisites:** Python 3.10 or later installed on your machine.
No third-party packages are required (the project intentionally uses
only the Python standard library, so `requirements.txt` is empty by
design — see the file for confirmation).

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/<your-repo-name>.git
   cd <your-repo-name>
   ```

2. **(Optional but recommended) create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   (This is a no-op today since no external packages are used, but is
   included for completeness / future extensions.)

## Running the Project

From the project root, run:

```bash
python3 -m src.main
```

On first run, no users exist yet, so the program will walk you
through creating the first **admin** account, then log you in. After
that, use the numbered menu to navigate between Student Management,
Subject Management, Attendance, Grades, and Analytics & Reports.

### Example first session

```
Username: admin
Password (min 6 chars): admin123
```

Then from the main menu:
1. Go to **Subject Management → Add subject** and create a subject
   (e.g., code `CS101`, name `Intro to CS`, max marks `100`).
2. Go to **Student Management → Add student** and add a student.
3. Go to **Attendance → Mark attendance** and **Grades → Record marks**
   to add some data for that student.
4. Go to **Analytics & Reports → Individual student report** or
   **Full class summary** to see the generated analytics.

## Running Tests

```bash
python3 -m unittest discover -s tests -v
```

All tests use a temporary, isolated SQLite database, so they never
touch your real `data/school.db`.

## Non-Functional Requirements Addressed

- **Security** — passwords are salted and hashed, never stored in
  plain text.
- **Reliability** — all inputs are validated; a top-level exception
  handler in `main.py` prevents unexpected crashes.
- **Maintainability** — code is split into small, single-responsibility
  modules with docstrings explaining intent.
- **Logging/Monitoring** — a dedicated logging module records actions
  and errors with timestamps to `data/app.log`.
- **Scalability** — the `database.py` module isolates all SQL access
  behind functions, making it straightforward to swap SQLite for a
  server-based database (e.g., PostgreSQL) later without touching
  business logic.

## Notes

- `data/school.db` and `data/app.log` are generated automatically on
  first run and are excluded from version control via `.gitignore`.
- This project was built as a learning/portfolio project for a course
  evaluation. See `statement.md` for the full problem statement and
  scope, and `docs/` for design diagrams referenced in the project
  report.
