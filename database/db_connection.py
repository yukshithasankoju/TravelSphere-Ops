
import sqlite3
import os

# Find the main project folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database file location
DB_PATH = os.path.join(BASE_DIR, "database", "travelspere.db")

# Function to connect to the database
def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection
