
import pandas as pd
from database.db_connection import get_connection


# 1. Calculate performance for every branch
def calculate_branch_performance(branch_data):

    performance_data = branch_data.copy()

    performance_data["Achievement (%)"] = (
        performance_data["Revenue"] /
        performance_data["Target"] * 100
    ).round(2)

    performance_data["Target Difference"] = (
        performance_data["Revenue"] -
        performance_data["Target"]
    )

    performance_data["Status"] = performance_data[
        "Achievement (%)"
    ].apply(
        lambda value: "Achieved Target"
        if value >= 100
        else "Below Target"
    )

    performance_data = performance_data.sort_values(
        by="Achievement (%)",
        ascending=False
    )

    return performance_data


# 2. Identify the best and underperforming branches
def get_performance_summary(performance_data):

    best_branch = performance_data.iloc[0]

    underperforming = performance_data[
        performance_data["Achievement (%)"] < 100
    ]

    summary = {
        "best_branch": best_branch["Branch"],
        "best_achievement": best_branch["Achievement (%)"],
        "underperforming_count": len(underperforming)
    }

    return summary


# 3. Generate performance recommendations
def generate_recommendations(performance_data):

    recommendations = []

    underperforming = performance_data[
        performance_data["Achievement (%)"] < 100
    ]

    if len(underperforming) == 0:

        recommendations.append(
            "All branches have achieved their revenue targets."
        )

    else:

        for _, row in underperforming.iterrows():

            recommendations.append(
                f"{row['Branch']}: Revenue is "
                f"₹{abs(row['Target Difference']):,.0f} "
                f"below target. Review booking performance "
                f"and customer enquiries."
            )

    return recommendations
# Load branch records from SQLite database
# Load the latest branch records from SQLite database
def load_branch_data():
    connection = get_connection()

    query = """
        SELECT
            b.branch_name AS Branch,
            p.revenue AS Revenue,
            p.target AS Target,
            p.bookings AS Bookings,
            p.cancellations AS Cancellations,
            p.record_date AS Date
        FROM performance_records p
        JOIN branches b
            ON p.branch_id = b.branch_id
        WHERE b.is_active = 1
        AND p.record_date = (
            SELECT MAX(p2.record_date)
            FROM performance_records p2
            WHERE p2.branch_id = p.branch_id
        )
        ORDER BY b.branch_name
    """

    branch_data = pd.read_sql_query(query, connection)
    connection.close()

    return branch_data
    # 5. Identify branches that need attention

def identify_branch_alerts(performance_data):

    alerts = []

    for _, row in performance_data.iterrows():

        if row["Achievement (%)"] < 70:
            alerts.append({
                "Branch": row["Branch"],
                "Alert": "Critical Performance",
                "Message": "Branch is significantly below its revenue target."
            })

        elif row["Achievement (%)"] < 100:
            alerts.append({
                "Branch": row["Branch"],
                "Alert": "Performance Warning",
                "Message": "Branch has not achieved its revenue target."
            })

        else:
            alerts.append({
                "Branch": row["Branch"],
                "Alert": "Target Achieved",
                "Message": "Branch has achieved its revenue target."
            })

    return alerts
    # 6. Analyze daily revenue trends
def analyze_revenue_trends(history_data):

    trend_data = history_data.copy()

    trend_data = trend_data.sort_values(
        by=["Branch", "Date"]
    )

    trend_data["Previous Revenue"] = (
        trend_data.groupby("Branch")["Revenue"].shift(1)
    )

    trend_data["Revenue Change"] = (
        trend_data["Revenue"] - trend_data["Previous Revenue"]
    )

    trend_data["Revenue Change (%)"] = (
        trend_data["Revenue"]
        .pct_change()
    )

    trend_data["Revenue Change (%)"] = (
        trend_data.groupby("Branch")["Revenue"]
        .pct_change()
        .mul(100)
        .round(2)
    )

    trend_data["Trend"] = trend_data["Revenue Change"].apply(
        lambda value: "Increased"
        if value > 0
        else "Decreased"
        if value < 0
        else "No Change"
    )

    return trend_data
    # 7. Analyze cancellation rates
def analyze_cancellation_trends(history_data):

    cancellation_data = history_data.copy()

    cancellation_data = cancellation_data.sort_values(
        by=["Branch", "Date"]
    )

    cancellation_data["Cancellation Rate (%)"] = (
        cancellation_data["Cancellations"]
        .div(cancellation_data["Bookings"].replace(0, pd.NA))
        .mul(100)
        .round(2)
    )

    cancellation_data["Previous Cancellation Rate (%)"] = (
        cancellation_data.groupby("Branch")["Cancellation Rate (%)"]
        .shift(1)
    )

    cancellation_data["Rate Change (%)"] = (
        cancellation_data["Cancellation Rate (%)"]
        - cancellation_data["Previous Cancellation Rate (%)"]
    ).round(2)

    return cancellation_data