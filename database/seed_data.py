from database.db_connection import get_connection

def seed_data():
    connection = get_connection()
    cursor = connection.cursor()

    branches = [
        ("Mumbai", "Mumbai"),
        ("Pune", "Pune"),
        ("Hyderabad", "Hyderabad"),
        ("Nagpur", "Nagpur"),
        ("Bengaluru", "Bengaluru")
    ]

    performance = [
        # Mumbai
        ("Mumbai", "2026-11-15", 380000, 400000, 175, 10),
        ("Mumbai", "2026-11-16", 410000, 400000, 190, 11),
        ("Mumbai", "2026-11-17", 430000, 400000, 200, 10),
        ("Mumbai", "2026-11-18", 450000, 400000, 210, 12),

        # Pune
        ("Pune", "2026-11-15", 320000, 400000, 150, 8),
        ("Pune", "2026-11-16", 340000, 400000, 160, 9),
        ("Pune", "2026-11-17", 360000, 400000, 170, 8),
        ("Pune", "2026-11-18", 380000, 400000, 175, 9),

        # Hyderabad
        ("Hyderabad", "2026-11-15", 350000, 400000, 160, 12),
        ("Hyderabad", "2026-11-16", 380000, 400000, 175, 13),
        ("Hyderabad", "2026-11-17", 400000, 400000, 185, 14),
        ("Hyderabad", "2026-11-18", 420000, 400000, 190, 15),

        # Nagpur
        ("Nagpur", "2026-11-15", 220000, 350000, 95, 16),
        ("Nagpur", "2026-11-16", 230000, 350000, 100, 17),
        ("Nagpur", "2026-11-17", 240000, 350000, 105, 18),
        ("Nagpur", "2026-11-18", 250000, 350000, 110, 18),

        # Bengaluru
        ("Bengaluru", "2026-11-15", 420000, 420000, 140, 6),
        ("Bengaluru", "2026-11-16", 450000, 420000, 150, 7),
        ("Bengaluru", "2026-11-17", 480000, 420000, 155, 6),
        ("Bengaluru", "2026-11-18", 500000, 420000, 160, 7),
    ]
    # Insert branches if they do not already exist
    for branch_name, city in branches:
        cursor.execute(
            "INSERT OR IGNORE INTO branches (branch_name, city) VALUES (?, ?)",
            (branch_name, city)
        )

    # Insert performance records if they do not already exist
    for record in performance:
        branch_name, record_date, revenue, target, bookings, cancellations = record

        cursor.execute(
            "SELECT branch_id FROM branches WHERE branch_name = ?",
            (branch_name,)
        )
        branch = cursor.fetchone()

        if branch:
            cursor.execute(
                """
                SELECT record_id FROM performance_records
                WHERE branch_id = ? AND record_date = ?
                """,
                (branch["branch_id"], record_date)
            )

            existing_record = cursor.fetchone()

            if not existing_record:
                cursor.execute(
                    """
                    INSERT INTO performance_records
                    (branch_id, record_date, revenue, target, bookings, cancellations)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        branch["branch_id"],
                        record_date,
                        revenue,
                        target,
                        bookings,
                        cancellations
                    )
                )

    connection.commit()
    connection.close()

    print("Sample branch data inserted successfully!")


if __name__ == "__main__":
    seed_data()
