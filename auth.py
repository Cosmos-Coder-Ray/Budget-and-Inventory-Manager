import hashlib
from db import create_connection

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    """Register a new user"""
    connection = create_connection()
    if not connection:
        return False, "Database connection failed"
    
    try:
        cursor = connection.cursor()
        hashed_password = hash_password(password)
        
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                      (username, hashed_password))
        connection.commit()
        connection.close()
        return True, "User registered successfully!"
        
    except Exception as e:
        connection.close()
        return False, f"Registration failed: {str(e)}"

def login_user(username, password):
    """Login user and return user_id if successful"""
    connection = create_connection()
    if not connection:
        return False, "Database connection failed"
    
    try:
        cursor = connection.cursor()
        hashed_password = hash_password(password)
        
        cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", 
                      (username, hashed_password))
        result = cursor.fetchone()
        connection.close()
        
        if result:
            return True, result[0]  # Return user_id
        else:
            return False, "Invalid username or password"
            
    except Exception as e:
        connection.close()
        return False, f"Login failed: {str(e)}"

def user_exists(username):
    """Check if username already exists"""
    connection = create_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        connection.close()
        return result is not None
        
    except Exception as e:
        connection.close()
        return False 