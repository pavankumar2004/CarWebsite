import sqlite3
import bcrypt

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create a table to store user credentials
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
