
import streamlit as st
import pandas as pd
import plotly.express as px
from agents.performance_agent import (
    load_branch_data,
    calculate_branch_performance,
    get_performance_summary,
    generate_recommendations,
    identify_branch_alerts,
    analyze_revenue_trends,
    analyze_cancellation_trends
)

from database.fetch_data import load_performance_history
from database.create_tables import create_tables
from database.seed_data import seed_data
# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="TravelSphere Ops",
    page_icon="✈️",
    layout="wide"
)

# DATABASE INITIALIZATION

try:
    create_tables()
    seed_data()

except Exception as e:
    st.error(f"Database initialization failed: {e}")
    st.stop()

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.main {
    background-color: #F5F7FB;
}

[data-testid="stSidebar"] {
    background-color: #101D3A;
}

[data-testid="stSidebar"] * {
    color: white;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label > div:first-child {
    display: none;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    background-color: transparent;
    padding: 9px 12px;
    border-radius: 7px;
    cursor: pointer;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background-color: #243B60;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label p {
    color: white;
    font-size: 14px;
}

.metric-card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #E5EAF2;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# LOAD BRANCH DATA THROUGH PYTHON AGENT
# ==========================================

try:
    branch_data = load_branch_data()
    history_data = load_performance_history()
    




except FileNotFoundError:
    st.error(
        "Branch data file not found. "
        "Please check data/branch_data.csv."
    )
    st.stop()

except Exception as error:
    st.error(f"Unable to load branch data: {error}")
    st.stop()


# ==========================================
# SIDEBAR NAVIGATION
# ==========================================

st.sidebar.title("✈️ TravelSphere Ops")

st.sidebar.caption(
    "Franchise Operations Intelligence"
)

st.sidebar.markdown("---")

pages = [
    "Home",
    "Outlet Performance Agent",
    "Inventory Agent",
    "Staff Agent",
    "Marketing Agent",
    "Audit Agent",
    "Franchise Intelligence Engine",
    "Dashboard & Reporting",
    "Notification & Workflow"
]

selected_page = st.sidebar.radio(
    "MAIN MENU",
    pages
)

st.sidebar.markdown("---")

st.sidebar.caption(
    "Agentic AI Franchise Management System"
)


# ==========================================
# HOME PAGE
# ==========================================

if selected_page == "Home":

    st.title("Welcome to TravelSphere Ops")

    st.write(
        "Centralised Agentic AI-powered "
        "Franchise Operations Intelligence Platform."
    )

    st.markdown("---")

    total_branches = len(branch_data)

    total_revenue = branch_data["Revenue"].sum()

    total_bookings = branch_data["Bookings"].sum()

    total_cancellations = branch_data["Cancellations"].sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Branches",
        total_branches
    )

    col2.metric(
        "Total Bookings",
        f"{total_bookings:,}"
    )

    col3.metric(
        "Total Revenue",
        f"₹{total_revenue / 100000:.2f} L"
    )

    col4.metric(
        "Cancellations",
        total_cancellations
    )

    st.markdown("---")

    st.subheader("Branch Revenue Overview")

    revenue_chart = px.bar(
        branch_data,
        x="Branch",
        y=["Revenue", "Target"],
        barmode="group",
        title="Revenue vs Revenue Target",
        color_discrete_sequence=["#3679D8", "#AAB8CC"]
    )

    st.plotly_chart(
        revenue_chart,
        use_container_width=True
    )

    st.subheader("Quick Access")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("Outlet Performance Agent")

    with col2:
        st.info("Inventory Agent")

    with col3:
        st.info("Staff Agent")

    col4, col5, col6 = st.columns(3)

    with col4:
        st.info("Marketing Agent")

    with col5:
        st.info("Audit Agent")

    with col6:
        st.info("Franchise Intelligence Engine")


# ==========================================
# OUTLET PERFORMANCE AGENT
# ==========================================

elif selected_page == "Outlet Performance Agent":

    st.title("Outlet Performance Agent")

    st.write(
        "Monitor, compare and analyse franchise branch performance."
    )

    st.markdown("---")

    # BRANCH SELECTION

    st.subheader("Individual Branch Analysis")

    selected_branch = st.selectbox(
        "Select a Branch",
        branch_data["Branch"].tolist()
    )

    selected_data = branch_data[
        branch_data["Branch"] == selected_branch
    ].iloc[0]

    revenue = selected_data["Revenue"]
    target = selected_data["Target"]
    bookings = selected_data["Bookings"]
    cancellations = selected_data["Cancellations"]

    achievement = (revenue / target) * 100

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Revenue",
        f"₹{revenue:,.0f}"
    )

    col2.metric(
        "Revenue Target",
        f"₹{target:,.0f}"
    )

    col3.metric(
        "Bookings",
        int(bookings)
    )

    col4.metric(
        "Cancellations",
        int(cancellations)
    )

    st.subheader("Target Achievement")

    st.progress(
        min(float(achievement / 100), 1.0)
    )

    st.write(
        f"Target Achievement: {achievement:.2f}%"
    )

    if achievement >= 100:
        st.success(
            f"{selected_branch} has achieved its revenue target."
        )
    else:
        st.warning(
            f"{selected_branch} is below its revenue target."
        )

    st.markdown("---")

    # BRANCH PERFORMANCE COMPARISON

    st.subheader("Branch Performance Comparison")

    performance_data = calculate_branch_performance(
        branch_data
    )

    st.dataframe(
        performance_data,
        use_container_width=True,
        hide_index=True
    )
       # REVENUE TREND ANALYSIS

    st.markdown("---")

    st.subheader("Daily Revenue Trend")

    # DATE FILTER

    history_data["Date"] = pd.to_datetime(history_data["Date"])

    min_date = history_data["Date"].min().date()
    max_date = history_data["Date"].max().date()

    selected_dates = st.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    start_date, end_date = selected_dates

    filtered_history = history_data[
        (history_data["Date"].dt.date >= start_date) &
        (history_data["Date"].dt.date <= end_date)
    ]

    revenue_trend_data = analyze_revenue_trends(filtered_history)

    revenue_trend_chart = px.line(
        revenue_trend_data,
        x="Date",
        y="Revenue",
        color="Branch",
        markers=True,
        title="Daily Revenue Trend by Branch"
    )

    revenue_trend_chart.update_layout(
        xaxis_title="Date",
        yaxis_title="Revenue (₹)",
        hovermode="x unified"
    )

    st.plotly_chart(
        revenue_trend_chart,
        use_container_width=True
    )

    # BOOKING TREND ANALYSIS

    st.markdown("---")

    st.subheader("Daily Booking Trend")

    booking_trend_chart = px.line(
        filtered_history,
        x="Date",
        y="Bookings",
        color="Branch",
        markers=True,
        title="Daily Bookings by Branch"
    )

    booking_trend_chart.update_layout(
        xaxis_title="Date",
        yaxis_title="Number of Bookings",
        hovermode="x unified"
    )

    st.plotly_chart(
        booking_trend_chart,
        use_container_width=True
    )
        # HISTORICAL PERFORMANCE REPORT

    st.markdown("---")

    st.subheader("Download Historical Performance Report")

    historical_csv = filtered_history.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Historical Report CSV",
        data=historical_csv,
        file_name="historical_performance_report.csv",
        mime="text/csv"
    )
    # BRANCH BOOKING COMPARISON

    st.markdown("---")

    st.subheader("Branch-wise Booking Comparison")

    booking_comparison = performance_data.sort_values(
        by="Bookings",
        ascending=False
    )

    booking_comparison_chart = px.bar(
        booking_comparison,
        x="Branch",
        y="Bookings",
        text="Bookings",
        title="Bookings Comparison Across Branches",
        color="Branch"
    )

    booking_comparison_chart.update_layout(
        xaxis_title="Branch",
        yaxis_title="Total Bookings",
        showlegend=False
    )

    st.plotly_chart(
        booking_comparison_chart,
        use_container_width=True
    )
           # BOOKING INSIGHTS

    st.markdown("---")

    st.subheader("Booking Insights")

    total_bookings = performance_data["Bookings"].sum()

    highest_booking_branch = performance_data.loc[
        performance_data["Bookings"].idxmax()
    ]

    lowest_booking_branch = performance_data.loc[
        performance_data["Bookings"].idxmin()
    ]

    average_bookings = performance_data["Bookings"].mean()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Bookings", int(total_bookings))

    with col2:
        st.metric(
            "Highest Bookings",
            highest_booking_branch["Branch"],
            int(highest_booking_branch["Bookings"])
        )

    with col3:
        st.metric(
            "Lowest Bookings",
            lowest_booking_branch["Branch"],
            int(lowest_booking_branch["Bookings"])
        )

    with col4:
        st.metric("Average Bookings", round(average_bookings, 2))


    # AUTOMATIC BOOKING OBSERVATIONS

    st.markdown("---")

    st.subheader("Automatic Booking Observations")

    booking_difference = (
        highest_booking_branch["Bookings"]
        - lowest_booking_branch["Bookings"]
    )

    st.info(
        f"{highest_booking_branch['Branch']} leads with "
        f"{int(highest_booking_branch['Bookings'])} bookings, "
        f"while {lowest_booking_branch['Branch']} has the lowest "
        f"with {int(lowest_booking_branch['Bookings'])} bookings. "
        f"The difference between them is "
        f"{int(booking_difference)} bookings."
    )

    if average_bookings > 0:

        below_average_branches = performance_data[
            performance_data["Bookings"] < average_bookings
        ]

        if not below_average_branches.empty:

            st.warning(
                "Branches performing below the booking average: "
                + ", ".join(
                    below_average_branches["Branch"].tolist()
                )
            )

        else:

            st.success(
                "All branches are performing at or above "
                "the booking average."
            )


    # OVERALL OUTLET PERFORMANCE SUMMARY

    st.markdown("---")

    st.subheader("Overall Outlet Performance Summary")

    total_revenue = performance_data["Revenue"].sum()
    total_target = performance_data["Target"].sum()
    total_cancellations = performance_data["Cancellations"].sum()

    overall_achievement = (
        total_revenue / total_target * 100
        if total_target > 0 else 0
    )

    overall_cancellation_rate = (
        total_cancellations / total_bookings * 100
        if total_bookings > 0 else 0
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Revenue",
            f"₹{total_revenue:,.0f}"
        )

    with col2:
        st.metric(
            "Overall Target Achievement",
            f"{overall_achievement:.2f}%"
        )

    with col3:
        st.metric(
            "Total Bookings",
            int(total_bookings)
        )

    col4, col5, col6 = st.columns(3)

    with col4:
        st.metric(
            "Total Target",
            f"₹{total_target:,.0f}"
        )

    with col5:
        st.metric(
            "Total Cancellations",
            int(total_cancellations)
        )

    with col6:
        st.metric(
            "Overall Cancellation Rate",
            f"{overall_cancellation_rate:.2f}%"
        )


    # MANAGEMENT DECISION INSIGHTS

    st.markdown("---")

    st.subheader("Management Decision Insights")

    if overall_achievement >= 100:

        st.success(
            "Overall Status: On Target. "
            "Revenue has met or exceeded the combined target."
        )

    elif overall_achievement >= 80:

        st.warning(
            "Overall Status: Needs Improvement. "
            "Revenue is progressing but the combined target "
            "has not been achieved."
        )

    else:

        st.error(
            "Overall Status: Below Target. "
            "Revenue performance requires management attention."
        )

    if overall_cancellation_rate > 10:

        st.warning(
            f"Cancellation rate is "
            f"{overall_cancellation_rate:.2f}%. "
            "Management should review cancellation patterns "
            "and identify possible causes."
        )

    else:

        st.success(
            f"Cancellation rate is "
            f"{overall_cancellation_rate:.2f}%. "
            "Continue monitoring cancellations across branches."
        )
    # PERFORMANCE SUMMARY

    st.subheader("Performance Highlights")

    summary = get_performance_summary(
        performance_data
    )

    col1, col2 = st.columns(2)

    with col1:
        st.success(
            f"Best Performing Branch: "
            f"{summary['best_branch']} "
            f"({summary['best_achievement']:.2f}% achieved)"
        )

    with col2:
        st.warning(
            f"Branches Below Target: "
            f"{summary['underperforming_count']}"
        )
    # BRANCH PERFORMANCE ALERTS

    st.markdown("---")

    st.subheader("Branch Performance Alerts")

    alerts = identify_branch_alerts(performance_data)

    for alert in alerts:

        st.write(f"**{alert['Branch']}**")

        if alert["Alert"] == "Critical Performance":
            st.error(alert["Message"])

        elif alert["Alert"] == "Performance Warning":
            st.warning(alert["Message"])

        else:
            st.success(alert["Message"])
    # PERFORMANCE RECOMMENDATIONS

    st.markdown("---")

    st.subheader("Performance Recommendations")

    recommendations = generate_recommendations(
        performance_data
    )

    for recommendation in recommendations:
        st.warning(recommendation)

    # BRANCH-SPECIFIC RECOMMENDATIONS

    st.markdown("---")

    st.subheader("Branch-wise Action Plan")

    for _, row in performance_data.iterrows():

        branch_name = row["Branch"]
        revenue = row["Revenue"]
        target = row["Target"]
        bookings = row["Bookings"]
        cancellations = row["Cancellations"]

        achievement = (
            revenue / target * 100
            if target > 0 else 0
        )

        cancellation_rate = (
            cancellations / bookings * 100
            if bookings > 0 else 0
        )

        st.markdown(f"### {branch_name}")

        if achievement < 70:

            st.error(
                f"Revenue achievement is {achievement:.2f}%. "
                "Review sales performance and identify reasons "
                "for the revenue gap."
            )

        elif achievement < 100:

            st.warning(
                f"Revenue achievement is {achievement:.2f}%. "
                "Focus on closing the remaining target gap."
            )

        else:

            st.success(
                f"Target achieved with {achievement:.2f}%. "
                "Maintain the current performance."
            )

        if cancellation_rate > 10:

            st.warning(
                f"Cancellation rate is {cancellation_rate:.2f}%. "
                "Investigate cancellation reasons and booking issues."
            )

        else:

            st.info(
                f"Cancellation rate: {cancellation_rate:.2f}%. "
                "Continue monitoring booking quality."
            )


    # CANCELLATION ANALYSIS

    st.markdown("---")

    st.subheader("Cancellation Analysis")

    cancellation_chart = px.bar(
        branch_data,
        x="Branch",
        y="Cancellations",
        title="Branch-wise Cancellations",
        text="Cancellations",
        color="Cancellations",
        color_continuous_scale="Blues"
    )

    cancellation_chart.update_traces(
        textposition="outside"
    )

    cancellation_chart.update_layout(
        xaxis_title="Branch",
        yaxis_title="Number of Cancellations"
    )

    st.plotly_chart(
        cancellation_chart,
        use_container_width=True
    )


    # CANCELLATION RATE TREND ANALYSIS

    st.markdown("---")

    st.subheader("Daily Cancellation Rate Trend")

    cancellation_trend_data = analyze_cancellation_trends(filtered_history)

    cancellation_trend_chart = px.line(
        cancellation_trend_data,
        x="Date",
        y="Cancellation Rate (%)",
        color="Branch",
        markers=True,
        title="Daily Cancellation Rate by Branch"
    )

    cancellation_trend_chart.update_layout(
        xaxis_title="Date",
        yaxis_title="Cancellation Rate (%)",
        hovermode="x unified"
    )

    st.plotly_chart(
        cancellation_trend_chart,
        use_container_width=True
    )

# ==========================================
# INVENTORY AGENT
# ==========================================

elif selected_page == "Inventory Agent":

    st.title("Inventory Agent")

    st.write(
        "Monitor travel package availability, "
        "hotel rooms, transport seats and tour slots."
    )

    st.info(
        "Inventory tracking and demand prediction "
        "will be developed in the next phase."
    )


# ==========================================
# STAFF AGENT
# ==========================================

elif selected_page == "Staff Agent":

    st.title("Staff Agent")

    st.write(
        "Monitor employee attendance, schedules, "
        "workload and productivity."
    )

    st.info(
        "Staff management and productivity analysis "
        "will be developed in the next phase."
    )


# ==========================================
# MARKETING AGENT
# ==========================================

elif selected_page == "Marketing Agent":

    st.title("Marketing Agent")

    st.write(
        "Analyse marketing campaigns, customer enquiries, "
        "conversions and promotion effectiveness."
    )

    st.info(
        "Campaign analysis and marketing recommendations "
        "will be developed in the next phase."
    )


# ==========================================
# AUDIT AGENT
# ==========================================

elif selected_page == "Audit Agent":

    st.title("Audit Agent")

    st.write(
        "Monitor operational procedures, booking records "
        "and franchise compliance."
    )

    st.info(
        "Audit monitoring and compliance checks "
        "will be developed in the next phase."
    )


# ==========================================
# FRANCHISE INTELLIGENCE ENGINE
# ==========================================

elif selected_page == "Franchise Intelligence Engine":

    st.title("Franchise Intelligence Engine")

    st.write(
        "Central intelligence system responsible for "
        "coordinating specialist agents."
    )

    st.info(
        "Agent coordination and central decision-making "
        "will be developed in a later phase."
    )


# ==========================================
# DASHBOARD AND REPORTING
# ==========================================

elif selected_page == "Dashboard & Reporting":

    st.title("Dashboard & Reporting")

    st.write(
        "View centralised franchise reports and "
        "business performance information."
    )

    st.dataframe(
        branch_data,
        use_container_width=True,
        hide_index=True
    )
        # DOWNLOAD PERFORMANCE REPORT

    st.markdown("---")

    st.subheader("Download Performance Report")

    report_csv = performance_data.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Branch Performance CSV",
        data=report_csv,
        file_name="outlet_performance_report.csv",
        mime="text/csv"
    )


# ==========================================
# NOTIFICATION AND WORKFLOW
# ==========================================

elif selected_page == "Notification & Workflow":

    st.title("Notification & Workflow")

    st.write(
        "Manage alerts, notifications, escalations "
        "and recommended action plans."
    )

    st.info(
        "Automated notification and workflow features "
        "will be developed in a later phase."
    )
