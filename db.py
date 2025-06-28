import sqlite3
import os

def create_connection():
    try:
        # Create database file if it doesn't exist
        db_file = 'wizard_test.db'
        connection = sqlite3.connect(db_file)
        print(f'Connected to SQLite database: {db_file}')
        return connection
    except Exception as e:
        print(f'Error: {e}')
        return None

def create_tables(connection):
    try:
        cursor = connection.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        
        # Create expenses table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Create products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price REAL NOT NULL,
                stock INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        connection.commit()
        print("Tables created successfully!")
        
    except Exception as e:
        print(f'Error creating tables: {e}')

def init_database():
    connection = create_connection()
    if connection:
        create_tables(connection)
        connection.close()
        return True
    return False 