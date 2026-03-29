import sqlite3
from config import DATABASE_NAME


class ResultsDatabase:
    def __init__(self):
        self.db_name = DATABASE_NAME
        self._init()

    def _init(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS results (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                sno         TEXT,
                course_code TEXT,
                course_name TEXT,
                grade       TEXT,
                status      TEXT,
                month_year  TEXT,
                scraped_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(course_code, grade)
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                course_code TEXT,
                course_name TEXT,
                grade       TEXT,
                notified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
        print("[✓] Database ready")

    def get_all_results(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('SELECT course_code, grade FROM results')
        rows = c.fetchall()
        conn.close()
        return {f"{r[0]}_{r[1]}": True for r in rows}

    def find_new_results(self, current_results):
        existing = self.get_all_results()
        return [r for r in current_results
                if f"{r['course_code']}_{r['grade']}" not in existing]

    def add_result(self, result):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute('''
                INSERT OR IGNORE INTO results
                (sno, course_code, course_name, grade, status, month_year)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (result['sno'], result['course_code'], result['course_name'],
                  result['grade'], result['status'], result['month_year']))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[✗] DB add error: {e}")

    def log_notification(self, course_code, course_name, grade):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute('''
                INSERT INTO notifications (course_code, course_name, grade)
                VALUES (?, ?, ?)
            ''', (course_code, course_name, grade))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[✗] DB log error: {e}")