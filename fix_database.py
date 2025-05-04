import sqlite3
import hashlib
import os

def hash_password(password):
    """Hash the password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def fix_database():
    # Remove existing database if it exists
    if os.path.exists('users.db'):
        os.remove('users.db')
        print("Removed existing database")
    
    # Create new database
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    # Create users table with correct schema
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, 
                  password TEXT,
                  emergency_name TEXT,
                  emergency_phone TEXT,
                  emergency_email TEXT)''')
    
    # Add test user
    username = "Nilopher"
    password = "Nilopher123"
    emergency_name = "Emergency Contact"
    emergency_phone = "+1234567890"
    emergency_email = "emergency@example.com"
    
    try:
        c.execute("""INSERT INTO users 
                    (username, password, emergency_name, emergency_phone, emergency_email) 
                    VALUES (?, ?, ?, ?, ?)""",
                 (username, hash_password(password), emergency_name, emergency_phone, emergency_email))
        conn.commit()
        print("Test user added successfully!")
        
        # Verify the user was added
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        if user:
            print("User verification successful!")
            print(f"Username: {user[0]}")
            print(f"Emergency Contact: {user[2]}")
        else:
            print("Error: User not found in database!")
            
    except sqlite3.IntegrityError as e:
        print(f"Error adding user: {str(e)}")
    finally:
        conn.close()

if __name__ == "__main__":
    fix_database() 