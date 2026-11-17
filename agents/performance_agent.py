
import pandas as pd


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
from pathlib import Path


# Load branch records from CSV
def load_branch_data():

    project_folder = Path(__file__).resolve().parent.parent

    file_path = project_folder / "data" / "branch_data.csv"

    branch_data = pd.read_csv(file_path)

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