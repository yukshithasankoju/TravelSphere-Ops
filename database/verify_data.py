from db_connection import get_connection


def verify_data():
    connection = get_connection()
    cursor = connection.cursor()

    print("\n========== BRANCHES ==========\n")

    cursor.execute("SELECT * FROM branches")

    branches = cursor.fetchall()

    for branch in branches:
        print(dict(branch))

    print("\n===== PERFORMANCE RECORDS =====\n")

    cursor.execute("""
        SELECT
            b.branch_name,
            p.record_date,
            p.revenue,
            p.target,
            p.bookings,
            p.cancellations
        FROM performance_records p
        JOIN branches b
        ON p.branch_id = b.branch_id
        ORDER BY b.branch_name
    """)

    records = cursor.fetchall()

    for record in records:
        print(dict(record))

    print(f"\nTotal branches: {len(branches)}")
    print(f"Total performance records: {len(records)}")

    connection.close()


if __name__ == "__main__":
    verify_data()