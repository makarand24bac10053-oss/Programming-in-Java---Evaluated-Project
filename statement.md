# Problem Statement

## Problem Statement

Teachers and academic coordinators in small institutions and coaching
centers often track student attendance and grades using scattered
spreadsheets or paper registers. This makes it slow and error-prone to
answer a simple but important question: **which students need help
right now, and why?** There is no single, lightweight tool that
consolidates attendance and academic performance into one place and
automatically flags students who are falling behind.

## Scope of the Project

This project delivers a command-line application that lets an
administrator or teacher:

- Maintain a roster of students and the subjects offered.
- Record daily attendance per student per subject.
- Record marks for assessments (quizzes, midterms, finals, etc.).
- Generate analytics that combine attendance and marks to flag
  "at-risk" students using configurable thresholds.

**Out of scope** for this version: multi-institution support, a web
or mobile front-end, email/SMS notifications, and role-based
permission granularity beyond `admin` vs `teacher`. These are noted as
future enhancements in the project report.

## Target Users

- **Teachers**, who need to quickly log attendance and marks for their
  classes and see which of their students need attention.
- **Administrators**, who need an overview of a whole cohort's
  performance to plan interventions (extra classes, counselling,
  parent meetings).

## High-Level Features

1. **Authentication** — secure login for admin/teacher roles.
2. **Student Management** — full CRUD on student records.
3. **Subject Management** — define subjects and their grading scale.
4. **Attendance Tracking** — per-date, per-subject attendance with
   automatic percentage calculation.
5. **Grades Tracking** — per-assessment marks with automatic average
   calculation.
6. **Analytics & Reporting** — individual and class-wide reports that
   surface attendance %, average marks %, and an automatic at-risk
   flag based on configurable thresholds (default: attendance below
   75%, or average marks below 40%).
