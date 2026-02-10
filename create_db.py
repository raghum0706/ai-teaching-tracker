import sqlite3

def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    # Unified Users Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT -- 'teacher' or 'student'
    )
    """)

    cur.execute("CREATE TABLE IF NOT EXISTS syllabus (id INTEGER PRIMARY KEY AUTOINCREMENT, teacher_id INTEGER, topic TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS timetable (id INTEGER PRIMARY KEY AUTOINCREMENT, teacher_id INTEGER, day INTEGER, topic TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS lecture_progress (id INTEGER PRIMARY KEY AUTOINCREMENT, teacher_id INTEGER, day INTEGER)")

    # Student Activity Tables (Placeholders)
    cur.execute("CREATE TABLE IF NOT EXISTS student_profiles (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, full_name TEXT, info TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS grades (id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER, subject TEXT, score TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS attendance (id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER, date TEXT, status TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS assignments (id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER, task TEXT, deadline TEXT)")

    # Seed default accounts
    try:
        cur.execute("INSERT INTO users (username, password, role) VALUES ('teacher', 'teacher123', 'teacher')")
        cur.execute("INSERT INTO users (username, password, role) VALUES ('student', 'student123', 'student')")
    except sqlite3.IntegrityError:
        pass 

    conn.commit()
    conn.close()
    print("Database Initialized.")

if __name__ == "__main__":
    init_db()