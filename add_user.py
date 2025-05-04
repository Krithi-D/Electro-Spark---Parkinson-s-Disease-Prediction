import sqlite3
import hashlib

def hash_password(password):
    """Hash the password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def add_user():
    # Connect to database
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    # Create table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, 
                  password TEXT,
                  emergency_name TEXT,
                  emergency_phone TEXT,
                  emergency_email TEXT)''')
    
    # User details
    username = "Nilopher"
    password = "Nilopher123"
    emergency_name = "Emergency Contact"  # You can update this
    emergency_phone = "+1234567890"  # You can update this
    emergency_email = "emergency@example.com"  # You can update this
    
    try:
        # Insert user
        c.execute("""INSERT INTO users 
                    (username, password, emergency_name, emergency_phone, emergency_email) 
                    VALUES (?, ?, ?, ?, ?)""",
                 (username, hash_password(password), emergency_name, emergency_phone, emergency_email))
        conn.commit()
        print("User added successfully!")
    except sqlite3.IntegrityError:
        print("User already exists!")
    finally:
        conn.close()

if __name__ == "__main__":
    add_user() 