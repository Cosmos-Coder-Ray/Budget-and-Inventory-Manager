"""
Database connection and utility functions for Smart Budget and Inventory Manager
This module handles all database operations including connection, queries, and data validation
"""

import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG
import hashlib
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        """Initialize database connection"""
        self.connection = None
        self.connect()
    
    def connect(self):
        """Establish connection to MySQL database"""
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            if self.connection.is_connected():
                print("✓ Successfully connected to MySQL database")
                return True
        except Error as e:
            print(f"✗ Error connecting to MySQL: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("✓ Database connection closed")
    
    def execute_query(self, query, params=None):
        """Execute a query and return results"""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            # For SELECT queries, fetch results
            if query.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                cursor.close()
                return results
            else:
                # For INSERT, UPDATE, DELETE queries
                self.connection.commit()
                cursor.close()
                return True
                
        except Error as e:
            print(f"✗ Database error: {e}")
            return False
    
    def hash_password(self, password):
        """Hash password using SHA-256 for security"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def validate_user(self, username, password):
        """Validate user login credentials"""
        hashed_password = self.hash_password(password)
        query = "SELECT id, username FROM users WHERE username = %s AND password = %s"
        result = self.execute_query(query, (username, hashed_password))
        
        if result and len(result) > 0:
            return result[0]
        return None
    
    def create_user(self, username, password):
        """Create a new user account"""
        hashed_password = self.hash_password(password)
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        return self.execute_query(query, (username, hashed_password))
    
    def user_exists(self, username):
        """Check if username already exists"""
        query = "SELECT id FROM users WHERE username = %s"
        result = self.execute_query(query, (username,))
        return len(result) > 0 if result else False

# Global database manager instance
db = DatabaseManager() 