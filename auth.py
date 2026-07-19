import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):

    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    try:

        cursor.execute(
            "INSERT INTO users(username,password) VALUES (?,?)",
            (username, hash_password(password))
        )

        conn.commit()
        return True

    except:
        return False

    finally:
        conn.close()

def login_user(username, password):

    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, hash_password(password))
    )

    user = cursor.fetchone()

    conn.close()

    return user 
def get_user_id(username):

    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM users WHERE username=?",
        (username,)
    )

    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]

    return None