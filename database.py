import sqlite3
import os
import hashlib
import time

# ================= DATABASE PATH =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data.db")

# ================= INIT DATABASE =================
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # USERS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # USER CONFIG TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_configs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            chat_id TEXT,
            name_prefix TEXT,
            delay INTEGER,
            cookies TEXT,
            messages TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


# ================= PASSWORD =================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ================= USER AUTH =================
def create_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hash_password(password))
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def verify_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM users WHERE username = ? AND password = ?",
        (username, hash_password(password))
    )
    row = cursor.fetchone()
    conn.close()

    if row:
        return row[0]   # user_id
    return None


# ================= USER CONFIG =================
def get_user_config(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT chat_id, name_prefix, delay, cookies, messages FROM user_configs WHERE user_id = ?",
        (user_id,)
    )
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "chat_id": row[0],
            "name_prefix": row[1],
            "delay": row[2],
            "cookies": row[3],
            "messages": row[4]
        }

    return {
        "chat_id": "",
        "name_prefix": "",
        "delay": 5,
        "cookies": "",
        "messages": ""
    }


def update_user_config(user_id, chat_id, name_prefix, delay, cookies, messages):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM user_configs WHERE user_id = ?",
        (user_id,)
    )
    exists = cursor.fetchone()

    if exists:
        cursor.execute("""
            UPDATE user_configs
            SET chat_id=?, name_prefix=?, delay=?, cookies=?, messages=?
            WHERE user_id=?
        """, (chat_id, name_prefix, delay, cookies, messages, user_id))
    else:
        cursor.execute("""
            INSERT INTO user_configs
            (user_id, chat_id, name_prefix, delay, cookies, messages)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, chat_id, name_prefix, delay, cookies, messages))

    conn.commit()
    conn.close()


# ================= ADMIN PANEL =================
def get_all_users():
    """
    Admin ke liye: saare users laata hai
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, username, created_at FROM users ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()

    users = []
    for r in rows:
        users.append({
            "id": r[0],
            "username": r[1],
            "created_at": r[2]
        })
    return users


def delete_user(user_id):
    """
    Admin ke liye: user + uski config delete karta hai
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM user_configs WHERE user_id = ?", (user_id,))
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))

    conn.commit()
    conn.close()
    return True
