import sqlite3

# Create the database and table if not exists
def init_db():
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            phone TEXT PRIMARY KEY,
            student_id TEXT,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Save student details (insert or update)
def save_student(phone, student_id, password):
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute("""
        INSERT OR REPLACE INTO students (phone, student_id, password)
        VALUES (?, ?, ?)
    """, (phone, student_id, password))
    conn.commit()
    conn.close()

# Get student details
def get_student(phone):
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute("SELECT student_id, password FROM students WHERE phone=?", (phone,))
    row = c.fetchone()
    conn.close()
    return row
