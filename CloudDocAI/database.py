import sqlite3
from datetime import datetime
from config import DATABASE


def get_db_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    """Create database tables if they don't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER NOT NULL,

        filename TEXT NOT NULL,

        filepath TEXT NOT NULL,

        file_type TEXT NOT NULL,

        file_size INTEGER NOT NULL,

        upload_date TEXT NOT NULL,

        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()

# User Functions

def create_user(username, email, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (username, email, password)
        VALUES (?, ?, ?)
    """, (username, email, password))

    conn.commit()
    conn.close()


def get_user_by_email(email):
    conn = get_db_connection()

    user = conn.execute("""
        SELECT * FROM users
        WHERE email = ?
    """, (email,)).fetchone()

    conn.close()
    return user


def get_user_by_id(user_id):
    conn = get_db_connection()

    user = conn.execute("""
        SELECT * FROM users
        WHERE id = ?
    """, (user_id,)).fetchone()

    conn.close()
    return user

# Document Functions

def add_document(user_id, filename, filepath, file_type, file_size):
    conn = get_db_connection()
    cursor = conn.cursor()

    upload_date = datetime.now().strftime("%d %b %Y, %I:%M %p")

    cursor.execute("""
        INSERT INTO documents
        (
            user_id,
            filename,
            filepath,
            file_type,
            file_size,
            upload_date
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        filename,
        filepath,
        file_type,
        file_size,
        upload_date
    ))

    conn.commit()
    conn.close()

def get_documents(user_id):
    conn = get_db_connection()

    documents = conn.execute("""
        SELECT *
        FROM documents
        WHERE user_id = ?
        ORDER BY upload_date DESC
    """, (user_id,)).fetchall()

    conn.close()
    return documents


def get_document(document_id):
    conn = get_db_connection()

    document = conn.execute("""
        SELECT *
        FROM documents
        WHERE id = ?
    """, (document_id,)).fetchone()

    conn.close()
    return document


def delete_document(document_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM documents
        WHERE id = ?
    """, (document_id,))

    conn.commit()
    conn.close()


def search_documents(user_id, keyword):
    conn = get_db_connection()

    documents = conn.execute("""
        SELECT *
        FROM documents
        WHERE user_id = ?
        AND filename LIKE ?
        ORDER BY upload_date DESC
    """, (user_id, f"%{keyword}%")).fetchall()

    conn.close()
    return documents