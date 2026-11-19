from database.db_connection import get_connection

def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS branches (
            branch_id INTEGER PRIMARY KEY AUTOINCREMENT,
            branch_name TEXT UNIQUE NOT NULL,
            city TEXT,
            is_active INTEGER DEFAULT 1
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS performance_records (
            record_id INTEGER PRIMARY KEY AUTOINCREMENT,
            branch_id INTEGER NOT NULL,
            record_date TEXT NOT NULL,
            revenue REAL DEFAULT 0,
            target REAL DEFAULT 0,
            bookings INTEGER DEFAULT 0,
            cancellations INTEGER DEFAULT 0,
            FOREIGN KEY (branch_id) REFERENCES branches(branch_id)
        )
    """)
    cursor.execute("""
    CREATE UNIQUE INDEX IF NOT EXISTS unique_branch_date
    ON performance_records (branch_id, record_date)
""")

    connection.commit()
    connection.close()

    print("Database tables created successfully!")


if __name__ == "__main__":
    create_tables()
