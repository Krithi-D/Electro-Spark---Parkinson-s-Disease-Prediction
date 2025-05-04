import streamlit as st
import sqlite3
import hashlib
from pathlib import Path
import requests
from twilio.rest import Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None

def init_db():
    """Initialize the SQLite database for users"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, 
                  password TEXT,
                  emergency_name TEXT,
                  emergency_phone TEXT,
                  emergency_email TEXT)''')
    conn.commit()
    conn.close()

def hash_password(password):
    """Hash the password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password, emergency_name, emergency_phone, emergency_email):
    """Register a new user"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute("""INSERT INTO users 
                    (username, password, emergency_name, emergency_phone, emergency_email) 
                    VALUES (?, ?, ?, ?, ?)""",
                 (username, hash_password(password), emergency_name, emergency_phone, emergency_email))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_user(username, password):
    """Verify user credentials"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()
    
    if result and result[0] == hash_password(password):
        return True
    return False

def get_emergency_contacts(username):
    """Get emergency contacts for a user"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("""SELECT emergency_name, emergency_phone, emergency_email 
                 FROM users WHERE username = ?""", (username,))
    result = c.fetchone()
    conn.close()
    return result

def send_emergency_notification(username):
    """Send emergency notification to contacts"""
    contacts = get_emergency_contacts(username)
    if not contacts:
        return False
    
    emergency_name, emergency_phone, emergency_email = contacts
    
    # Initialize Twilio client
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    twilio_phone = os.getenv('TWILIO_PHONE_NUMBER')
    
    if account_sid and auth_token and twilio_phone:
        try:
            client = Client(account_sid, auth_token)
            
            # Send SMS
            if emergency_phone:
                message = client.messages.create(
                    body=f"EMERGENCY ALERT: {username} has received a positive Parkinson's disease detection result. Please check on them immediately.",
                    from_=twilio_phone,
                    to=emergency_phone
                )
            
            # Send email using a service like SendGrid (you'll need to implement this)
            if emergency_email:
                # Implement email sending logic here
                pass
                
            return True
        except Exception as e:
            print(f"Error sending notification: {str(e)}")
            return False
    return False

def login_page():
    """Display the login page"""
    st.title("⚡ Electro Spark - Login")
    
    # Initialize database
    init_db()
    
    # Create tabs for Login and Register
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.subheader("Login to Your Account")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", key="login_button"):
            if username and password:
                if verify_user(username, password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.success("Login successful!")
                    st.experimental_rerun()
                else:
                    st.error("Invalid username or password")
            else:
                st.warning("Please enter both username and password")
    
    with tab2:
        st.subheader("Create New Account")
        new_username = st.text_input("Choose Username", key="register_username")
        new_password = st.text_input("Choose Password", type="password", key="register_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
        
        st.subheader("Emergency Contact Information")
        emergency_name = st.text_input("Emergency Contact Name", key="emergency_name")
        emergency_phone = st.text_input("Emergency Contact Phone Number", key="emergency_phone")
        emergency_email = st.text_input("Emergency Contact Email", key="emergency_email")
        
        if st.button("Register", key="register_button"):
            if new_username and new_password and confirm_password:
                if new_password != confirm_password:
                    st.error("Passwords do not match")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters long")
                elif not emergency_name or not emergency_phone:
                    st.error("Please provide at least emergency contact name and phone number")
                else:
                    if register_user(new_username, new_password, emergency_name, emergency_phone, emergency_email):
                        st.success("Registration successful! Please switch to the Login tab to sign in.")
                    else:
                        st.error("Username already exists")
            else:
                st.warning("Please fill in all required fields")

def logout():
    """Logout the current user"""
    st.session_state.authenticated = False
    st.session_state.username = None
    st.experimental_rerun()

# Export the required functions
__all__ = ['login_page', 'logout', 'send_emergency_notification']

if __name__ == "__main__":
    if not st.session_state.authenticated:
        login_page()
    else:
        st.sidebar.write(f"Welcome, {st.session_state.username}!")
        if st.sidebar.button("Logout"):
            logout()
        st.experimental_rerun() 