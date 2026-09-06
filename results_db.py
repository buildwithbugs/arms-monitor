import sqlite3
from config import DATABASE_NAME


class ResultsDatabase:
    def __init__(self):
        self.db_name = DATABASE_NAME
        self._init()

    @staticmethod
    def _result_key(result):
        return (
            str(result.get("course_code") or "").strip(),
            str(result.get("course_name") or "").strip(),
            str(result.get("status") or "").strip(),
            str(result.get("grade") or "").strip(),
            str(result.get("course_gpa") or "").strip(),
        )

    def _ensure_table_columns(self, conn, table_name, columns):
        c = conn.cursor()
        c.execute(f"PRAGMA table_info({table_name})")
        existing = {row[1] for row in c.fetchall()}

        for column_name, column_sql in columns.items():
            if column_name not in existing:
                print(f"[DB] Adding missing column: {column_name}")
                c.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_sql}")

        conn.commit()

    def _init(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        c.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'notifications'")
        notifications_exists = c.fetchone() is not None
        if notifications_exists:
            print("[DB] Existing notifications table found")

        c.execute(
            '''
            CREATE TABLE IF NOT EXISTS results (
                id                   INTEGER PRIMARY KEY AUTOINCREMENT,
                course_code          TEXT,
                course_name          TEXT,
                course_type          TEXT,
                status               TEXT,
                grade                TEXT,
                attendance           TEXT,
                assessments          TEXT,
                other_requirements    TEXT,
                course_gpa           TEXT,
                scraped_at           TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            '''
        )
        c.execute(
            '''
            CREATE TABLE IF NOT EXISTS notifications (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                course_code     TEXT,
                course_name     TEXT,
                course_type     TEXT,
                status          TEXT,
                month_year      TEXT,
                attendance      TEXT,
                assessments     TEXT,
                other_requirements TEXT,
                grade           TEXT,
                course_gpa      TEXT,
                notified_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            '''
        )
        c.execute(
            '''
            CREATE TABLE IF NOT EXISTS monitor_state (
                state_key TEXT PRIMARY KEY,
                state_value TEXT NOT NULL
            )
            '''
        )
        conn.commit()

        self._ensure_table_columns(conn, "results", {
            "course_code": "TEXT",
            "course_name": "TEXT",
            "course_type": "TEXT",
            "status": "TEXT",
            "grade": "TEXT",
            "attendance": "TEXT",
            "assessments": "TEXT",
            "other_requirements": "TEXT",
            "course_gpa": "TEXT",
        })

        self._ensure_table_columns(conn, "notifications", {
            "course_type": "TEXT",
            "status": "TEXT",
            "month_year": "TEXT",
            "attendance": "TEXT",
            "assessments": "TEXT",
            "other_requirements": "TEXT",
            "course_gpa": "TEXT",
        })

        c.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS idx_results_identity ON results (course_code, course_name, status, grade, course_gpa)"
        )
        duplicate_notification_codes = c.execute(
            "SELECT course_code FROM notifications WHERE course_code IS NOT NULL AND TRIM(course_code) != '' GROUP BY course_code HAVING COUNT(*) > 1"
        ).fetchall()
        if duplicate_notification_codes:
            print("[DB] Existing duplicate notification course codes detected; preserving history and using application-level deduplication")
        else:
            try:
                c.execute(
                    "CREATE UNIQUE INDEX IF NOT EXISTS idx_notifications_course_code ON notifications (course_code)"
                )
                print("[DB] Notification course-code uniqueness index ready")
            except sqlite3.IntegrityError:
                print("[DB] Notification course-code uniqueness check skipped because existing rows conflict")

        conn.commit()
        conn.close()
        print("[DB] Database schema ready")

    def get_all_results(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute(
            "SELECT course_code, course_name, status, grade, course_gpa FROM results"
        )
        rows = c.fetchall()
        conn.close()
        return {self._result_key({
            "course_code": row[0],
            "course_name": row[1],
            "status": row[2],
            "grade": row[3],
            "course_gpa": row[4],
        }): True for row in rows}

    def get_notified_course_codes(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT course_code FROM notifications WHERE course_code IS NOT NULL AND TRIM(course_code) != ''")
        rows = c.fetchall()
        conn.close()
        return {str(row[0]).strip().upper() for row in rows}

    def get_state(self, state_key, default=None):
        conn = sqlite3.connect(self.db_name)
        row = conn.execute(
            "SELECT state_value FROM monitor_state WHERE state_key = ?",
            (state_key,),
        ).fetchone()
        conn.close()
        return row[0] if row else default

    def set_state(self, state_key, state_value):
        conn = sqlite3.connect(self.db_name)
        conn.execute(
            "INSERT OR REPLACE INTO monitor_state (state_key, state_value) VALUES (?, ?)",
            (state_key, str(state_value)),
        )
        conn.commit()
        conn.close()

    def find_new_results(self, current_results):
        existing_codes = self.get_notified_course_codes()
        return [
            result for result in current_results
            if str(result.get("course_code") or "").strip().upper() not in existing_codes
        ]

    def add_result(self, result):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute(
                '''
                INSERT OR IGNORE INTO results
                (course_code, course_name, course_type, status, grade, attendance, assessments, other_requirements, course_gpa)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                (
                    result.get("course_code", ""),
                    result.get("course_name", ""),
                    result.get("course_type", ""),
                    result.get("status", ""),
                    result.get("grade", ""),
                    result.get("attendance", ""),
                    result.get("assessments", ""),
                    result.get("other_requirements", ""),
                    result.get("course_gpa", ""),
                ),
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[✗] DB add error: {e}")

    def log_notification(
        self,
        course_code,
        course_name,
        course_type="",
        grade="",
        course_gpa="",
        status="",
        month_year="",
        attendance="",
        assessments="",
        other_requirements="",
    ):
        if not str(course_code or "").strip():
            return
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute(
                '''
                INSERT OR IGNORE INTO notifications (
                    course_code,
                    course_name,
                    course_type,
                    status,
                    month_year,
                    attendance,
                    assessments,
                    other_requirements,
                    grade,
                    course_gpa
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                (
                    str(course_code).strip(),
                    course_name,
                    course_type,
                    status,
                    month_year,
                    attendance,
                    assessments,
                    other_requirements,
                    grade,
                    course_gpa,
                ),
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[✗] DB log error: {e}")