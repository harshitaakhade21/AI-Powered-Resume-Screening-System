import sqlite3

def create_db():
    conn = sqlite3.connect("resumes.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            skills TEXT,
            education TEXT,
            experience TEXT,
            score INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def insert_resume(name, data, score):
    conn = sqlite3.connect("resumes.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO resumes (name, skills, education, experience, score)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        name,
        ', '.join(data["skills"]),
        ', '.join(data["education"]),
        ', '.join(data["experience"]),
        score
    ))
    conn.commit()
    conn.close()
