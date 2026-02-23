import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Incident Analytics Dashboard", layout="wide")

def load_data():
    try:
        conn = sqlite3.connect('incident_system.db')
        query = "SELECT * FROM tickets"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        return pd.DataFrame()

st.title("📊 Smart Incident Analytics Dashboard")
st.markdown("Real-time insights from the AI-powered Complaint NLU Engine.")

df = load_data()

if df.empty:
    st.info("No tickets have been submitted yet. Go to the main app to submit a complaint.")
else:
    # Convert 'created_at' to datetime
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['date'] = df['created_at'].dt.date

    # Top metrics
    total_tickets = len(df)
    escalated = df['escalation_flag'].sum()
    st.markdown(f"**Total Tickets Processed:** {total_tickets} &nbsp;|&nbsp; **Critical Escalations:** {escalated}")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Complaint Category Distribution")
        # Bar chart
        cat_counts = df['category'].value_counts()
        st.bar_chart(cat_counts)
        
    with col2:
        st.subheader("Priority Distribution")
        # Pie chart using matplotlib
        prio_counts = df['priority'].value_counts()
        fig, ax = plt.subplots()
        # Custom colors for priority
        colors = {'High': '#ef4444', 'Medium': '#f59e0b', 'Low': '#10b981'}
        ax.pie(prio_counts, labels=prio_counts.index, 
               autopct='%1.1f%%', startangle=140, 
               colors=[colors.get(x, '#64748b') for x in prio_counts.index])
        ax.axis('equal')  
        st.pyplot(fig)

    st.markdown("---")

    st.subheader("Daily Complaint Trend")
    # Line chart
    daily_counts = df.groupby('date').size()
    st.line_chart(daily_counts)

    st.markdown("---")

    # Show raw data optionally
    if st.checkbox("Show Raw Incident Data"):
    st.dataframe(df.sort_values(by='created_at', ascending=False).drop(columns=['id', 'reply_text']))
