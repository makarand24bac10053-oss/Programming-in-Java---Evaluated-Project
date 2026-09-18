# Design Documentation

These diagrams are written in Mermaid syntax. You can render them by
pasting into https://mermaid.live, or GitHub renders Mermaid code
blocks natively in Markdown files — use these as a starting point for
your project report; redraw/relabel them in your own words rather
than copy-pasting verbatim.

## 1. System Architecture

```mermaid
flowchart TB
    UI["CLI Layer (main.py)"] --> AUTH["Auth Module"]
    UI --> SM["Student Management"]
    UI --> SUB["Subject Management"]
    UI --> ATT["Attendance Module"]
    UI --> GR["Grades Module"]
    UI --> AN["Analytics Module"]

    AN --> SM
    AN --> ATT
    AN --> GR
    ATT --> SM
    ATT --> SUB
    GR --> SM
    GR --> SUB

    AUTH --> DB[("SQLite Database")]
    SM --> DB
    SUB --> DB
    ATT --> DB
    GR --> DB

    UI --> LOG["Logger (utils/logger.py)"]
    UI --> VAL["Validators (utils/validators.py)"]
```

## 2. Use Case Diagram

```mermaid
flowchart LR
    Admin((Admin))
    Teacher((Teacher))

    Admin --> UC1[Manage Users]
    Admin --> UC2[Manage Students]
    Admin --> UC3[Manage Subjects]
    Admin --> UC4[Mark Attendance]
    Admin --> UC5[Record Marks]
    Admin --> UC6[View Reports]

    Teacher --> UC2
    Teacher --> UC4
    Teacher --> UC5
    Teacher --> UC6
```

## 3. Process / Workflow Diagram

```mermaid
flowchart TD
    Start([Start]) --> Login{User exists?}
    Login -- No --> CreateAdmin[Create first admin account]
    CreateAdmin --> LoginForm
    Login -- Yes --> LoginForm[Login form]
    LoginForm --> Valid{Credentials valid?}
    Valid -- No --> LoginForm
    Valid -- Yes --> Menu[Main Menu]
    Menu --> Choice{Select module}
    Choice --> Students[Student Mgmt]
    Choice --> Subjects[Subject Mgmt]
    Choice --> Attendance[Attendance]
    Choice --> Grades[Grades]
    Choice --> Reports[Analytics]
    Students --> Menu
    Subjects --> Menu
    Attendance --> Menu
    Grades --> Menu
    Reports --> Menu
    Menu --> Exit([Exit])
```

## 4. Class / Component Diagram

```mermaid
classDiagram
    class Database {
        +get_connection()
        +initialize_database()
    }
    class Auth {
        +register_user()
        +login_user()
    }
    class StudentManagement {
        +add_student()
        +update_student()
        +delete_student()
        +list_students()
    }
    class SubjectManagement {
        +add_subject()
        +list_subjects()
    }
    class Attendance {
        +mark_attendance()
        +get_attendance_percentage()
    }
    class Grades {
        +record_marks()
        +get_average_percentage()
    }
    class Analytics {
        +build_student_report()
        +class_summary_report()
    }

    Auth --> Database
    StudentManagement --> Database
    SubjectManagement --> Database
    Attendance --> Database
    Attendance --> StudentManagement
    Attendance --> SubjectManagement
    Grades --> Database
    Grades --> StudentManagement
    Grades --> SubjectManagement
    Analytics --> StudentManagement
    Analytics --> Attendance
    Analytics --> Grades
```

## 5. Sequence Diagram — "Generate Individual Student Report"

```mermaid
sequenceDiagram
    actor User
    participant CLI as main.py
    participant AN as analytics.py
    participant ATT as attendance.py
    participant GR as grades.py
    participant DB as SQLite

    User->>CLI: Select "Individual student report"
    CLI->>AN: build_student_report(student_id)
    AN->>ATT: get_attendance_percentage(student_id)
    ATT->>DB: SELECT attendance rows
    DB-->>ATT: rows
    ATT-->>AN: attendance %
    AN->>GR: get_average_percentage(student_id)
    GR->>DB: SELECT marks rows
    DB-->>GR: rows
    GR-->>AN: average %
    AN-->>CLI: report dict (with risk flags)
    CLI-->>User: Display report
```

## 6. ER Diagram

```mermaid
erDiagram
    USERS {
        int user_id PK
        string username
        string password_hash
        string role
    }
    STUDENTS {
        int student_id PK
        string roll_number
        string name
        string email
        int enrolled_year
    }
    SUBJECTS {
        int subject_id PK
        string subject_code
        string subject_name
        int max_marks
    }
    ATTENDANCE {
        int attendance_id PK
        int student_id FK
        int subject_id FK
        string date
        string status
    }
    MARKS {
        int mark_id PK
        int student_id FK
        int subject_id FK
        string assessment_name
        float marks_obtained
    }

    STUDENTS ||--o{ ATTENDANCE : has
    SUBJECTS ||--o{ ATTENDANCE : has
    STUDENTS ||--o{ MARKS : has
    SUBJECTS ||--o{ MARKS : has
