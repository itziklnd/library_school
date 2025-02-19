import sqlite3
import pandas as pd

DB_PATH = "books.db"  # נתיב למסד הנתונים
EXCEL_PATH = "backend/DATA/books.xlsx"  # קובץ ה-Excel עם הנתונים

# פונקציה לפתיחת חיבור חדש למסד הנתונים
def get_db_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

# יצירת טבלה (אם לא קיימת)
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

# טעינת נתונים ראשוניים מ-Excel למסד הנתונים
def load_initial_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    # בדיקה אם הטבלה ריקה
    cursor.execute("SELECT COUNT(*) FROM books")
    count = cursor.fetchone()[0]

    if count == 0:  # רק אם אין נתונים נטען מה-Excel
        df = pd.read_excel(EXCEL_PATH)  # טעינת הנתונים מה-Excel
        for _, row in df.iterrows():
            cursor.execute("INSERT INTO books (title, author) VALUES (?, ?)", (row["title"], row["author"]))
        conn.commit()
        print("📥 הנתונים נטענו ממסד הנתונים בהצלחה!")

    conn.close()

# פונקציה להוספת ספר למסד הנתונים
def add_book(title, author):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
    conn.commit()
    conn.close()

# פונקציה לחיפוש ספרים לפי שם
def search_books(query):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT title, author FROM books WHERE title LIKE ?", ('%' + query + '%',))
    results = cursor.fetchall()
    conn.close()
    return results

# הפעלת יצירת טבלה + טעינת נתונים
create_table()
load_initial_data()
