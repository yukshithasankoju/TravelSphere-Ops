
import streamlit as st
import pandas as pd
import plotly.express as px

from agents.performance_agent import (
    load_branch_data,
    calculate_branch_performance,
    get_performance_summary,
    generate_recommendations,
    identify_branch_alerts
)


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="TravelSphere Ops",
    page_icon="✈️",
    layout="wide"
)


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
