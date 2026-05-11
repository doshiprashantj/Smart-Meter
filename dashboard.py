# ==========================================
# SMART METER ANALYTICS DASHBOARD
# ==========================================

# Import Libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Smart Meter Analytics",
    page_icon="⚡",
    layout="wide"
)

# ==========================================
# TITLE
# ==========================================

st.title("⚡ Smart Meter Consumer Analytics Dashboard")

st.markdown("""
### AI-Based Electricity Theft Detection System

This dashboard helps electricity distribution companies:
- Detect suspicious consumers
- Monitor smart meter behavior
- Reduce non-technical losses
- Improve inspection prioritization
""")

# ==========================================
# LOAD DATASET
# ==========================================

@st.cache_data
def load_data():
    return pd.read_csv("smart_meter_data.csv")

data = load_data()

# ==========================================
# DATA PREVIEW
# ==========================================

st.subheader("📂 Dataset Preview")
st.dataframe(data.head())

# ==========================================
# SIDEBAR FILTERS
# ==========================================

st.sidebar.header("🔍 Filters")

# Area Filter
selected_area = st.sidebar.selectbox(
    "Select Area",
    data['Area'].unique()
)

filtered_data = data[data['Area'] == selected_area]

# ==========================================
# KPI METRICS
# ==========================================

st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Consumers",
        len(filtered_data)
    )

with col2:
    st.metric(
        "Suspicious Consumers",
        filtered_data['Theft_Label'].sum()
    )

with col3:
    avg_consumption = round(
        filtered_data['Daily_Consumption'].mean(),
        2
    )

    st.metric(
        "Average Consumption",
        avg_consumption
    )

with col4:
    theft_percentage = round(
        (
            filtered_data['Theft_Label'].sum()
            / len(filtered_data)
        ) * 100,
        2
    )

    st.metric(
        "Suspicious %",
        f"{theft_percentage}%"
    )

# ==========================================
# CONSUMPTION DISTRIBUTION
# ==========================================

st.subheader("📈 Consumer Consumption Distribution")

fig1 = px.histogram(
    filtered_data,
    x='Daily_Consumption',
    nbins=30,
    color='Theft_Label',
    title='Daily Electricity Consumption'
)

st.plotly_chart(fig1, use_container_width=True)

# ==========================================
# AREA-WISE ANALYTICS
# ==========================================

st.subheader("🌍 Area Wise Suspicious Consumers")

area_analysis = data.groupby('Area')['Theft_Label'].sum().reset_index()

fig2 = px.bar(
    area_analysis,
    x='Area',
    y='Theft_Label',
    title='Suspicious Consumers by Area'
)

st.plotly_chart(fig2, use_container_width=True)

# ==========================================
# HIGH RISK CONSUMERS
# ==========================================

st.subheader("🚨 High Risk Consumers")

high_risk = filtered_data[
    filtered_data['Theft_Label'] == 1
]

st.dataframe(
    high_risk[[
        'Consumer_ID',
        'Area',
        'Daily_Consumption',
        'Peak_Hour_Usage',
        'Billing_Amount',
        'Payment_Delay'
    ]]
)

# ==========================================
# POWER FACTOR ANALYSIS
# ==========================================

st.subheader("⚡ Power Factor Analysis")

fig3 = px.scatter(
    filtered_data,
    x='Voltage',
    y='Current',
    color='Theft_Label',
    size='Daily_Consumption',
    title='Voltage vs Current Analysis'
)

st.plotly_chart(fig3, use_container_width=True)

# ==========================================
# ALERT SYSTEM
# ==========================================

st.subheader("🚨 Preventive Inspection Alerts")

for index, row in high_risk.head(10).iterrows():

    st.warning(
        f"""
        ⚠ Suspicious Usage Detected
        
        Consumer ID: {row['Consumer_ID']}
        
        Area: {row['Area']}
        
        Daily Consumption: {row['Daily_Consumption']}
        """
    )

# ==========================================
# DOWNLOAD BUTTON
# ==========================================

st.subheader("⬇ Download Filtered Data")

csv = filtered_data.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download CSV",
    data=csv,
    file_name='filtered_smart_meter_data.csv',
    mime='text/csv'
)

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.markdown("""
### Hackathon Project

Smart Meter Consumer Analytics and Electricity Theft Detection System

Developed using:
- Python
- Streamlit
- pandas
- Plotly
- Machine Learning
""")
