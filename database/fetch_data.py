
import pandas as pd
from database.db_connection import get_connection


# Load all historical performance records
def load_performance_history():

    connection = get_connection()

    query = """
        SELECT
            b.branch_name AS Branch,
            p.record_date AS Date,
            p.revenue AS Revenue,
            p.target AS Target,
            p.bookings AS Bookings,
            p.cancellations AS Cancellations
        FROM performance_records p
        JOIN branches b
            ON p.branch_id = b.branch_id
        WHERE b.is_active = 1
        ORDER BY p.record_date ASC, b.branch_name ASC
    """

    history_data = pd.read_sql_query(query, connection)

    connection.close()

    return history_data


if __name__ == "__main__":
    data = load_performance_history()

    print(data)
    print("\nHistorical data loaded successfully!")
    print(f"Total records: {len(data)}")
