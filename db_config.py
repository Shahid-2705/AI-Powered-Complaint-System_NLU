import sqlite3
import os
from datetime import datetime

DATABASE_NAME = 'incident_system.db'

def get_db_connection():
    """Establish and return a connection to the SQLite database."""
    # Connect to the SQLite database (creates it if it doesn't exist)
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with the required schema."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create the tickets table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        complaint_text TEXT NOT NULL,
        category TEXT NOT NULL,
        sentiment TEXT NOT NULL,
        priority TEXT NOT NULL,
        department TEXT NOT NULL,
        escalation_flag BOOLEAN NOT NULL DEFAULT 0,
        reply_text TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

def insert_ticket(complaint_text, category, sentiment, priority, department, escalation_flag, reply_text=""):
    """Insert a new ticket into the schema."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO tickets (complaint_text, category, sentiment, priority, department, escalation_flag, reply_text)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (complaint_text, category, sentiment, priority, department, escalation_flag, reply_text))
    
    ticket_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return ticket_id

if __name__ == '__main__':
    init_db()
