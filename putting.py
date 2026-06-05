import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Golf Putting Tracker", page_icon="⛳", layout="centered")

st.title("⛳ Putting Stats Tracker")
st.write("Log your practice sessions directly to Google Sheets.")

# PASTE YOUR GOOGLE SHEET URL HERE
SQL_PUBLIC_URL = "https://docs.google.com/spreadsheets/d/1RysQbgIcLD2RDz_oaUdMx5tIJGR0X8UJe4a67X8yP68/edit?usp=sharing"

# Establish the connection to your Google Sheet
conn = st.connection("gsheets", type=GSheetsConnection)

# 1. Input Fields
drill = st.selectbox("Select Drill", ["6-Foot Gauge", "Ladder Drill", "Around the World", "Random Practice"])
distance = st.number_input("Distance (Feet)", min_value=1, max_value=100, value=6)
attempts = st.number_input("Balls Attempted", min_value=1, value=4)
made = st.number_input("Balls Made", min_value=0, max_value=int(attempts), value=0)

# 2. Log Data Button
if st.button("Log Round to Cloud", use_container_width=True):
    percentage = (made / attempts) * 100
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create a dataframe for the new row
    new_data = pd.DataFrame([{
        "Timestamp": timestamp,
        "Drill": drill,
        "Distance_Ft": distance,
        "Attempts": attempts,
        "Made": made,
        "Percentage": percentage
    }])
    
    try:
        # Read existing data safely
        existing_data = conn.read(spreadsheet=SQL_PUBLIC_URL, ttl=0)
        
        # Combine old data with new row
        updated_df = pd.concat([existing_data, new_data], ignore_index=True)
        
        # Update the Google Sheet
        conn.update(spreadsheet=SQL_PUBLIC_URL, data=updated_df)
        st.success(f"🚀 Sent to Google Sheets! Shot {percentage:.1f}% from {distance} feet.")
    except Exception as e:
        st.error(f"Error connecting to Google Sheets: {e}")

# 3. View Recent History
st.subheader("📋 Recent History (Live from Cloud)")
try:
    live_data = conn.read(spreadsheet=SQL_PUBLIC_URL, ttl=0)
    if not live_data.empty:
        st.dataframe(live_data.tail(5), use_container_width=True)
    else:
        st.info("No practice rounds logged yet.")
except Exception as e:
    st.warning("Could not load history preview.")
