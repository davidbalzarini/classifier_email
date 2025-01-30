import sqlite3
import os

class Database:
    def __init__(self):
        self.db_path = "emails.db"
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                classification TEXT NOT NULL,
                processed_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    def save_email(self, subject, classification):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO emails (subject, classification) VALUES (?, ?)",
            (subject, classification)
        )
        conn.commit()
        conn.close()
    
    def save_emails(self, emails):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.executemany(
            "INSERT INTO emails (subject, classification) VALUES (?, ?)",
            emails
        )
        conn.commit()
        conn.close()
    
    def get_processed_emails(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM emails ORDER BY processed_date DESC")
        emails = cursor.fetchall()
        conn.close()
        return emails