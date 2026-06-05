import streamlit as st
import pandas as pd
from datetime import datetime
import os

# File where data will be saved
DATA_FILE = "putting_data.csv"

# Initialize CSV file if it doesn't exist
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Timestamp", "Drill", "Distance_Ft", "Attempts", "Made", "Percentage"])
    df.to_csv(DATA_FILE, index=False)

st.title("⛳ Putting Stats Tracker")

# 1. Input Fields
drill = st.selectbox("Select Drill", ["6-Foot Gauge", "Ladder Drill", "Random Distance"])
distance = st.number_input("Distance (Feet)", min_value=1, max_value=100, value=6)
attempts = st.number_input("Balls Thrown/Attempted", min_value=1, value=4)
made = st.number_input("Balls Made", min_value=0, max_value=int(attempts), value=0)

# 2. Save Button
if st.button("Log Round"):
    percentage = (made / attempts) * 100
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create new row
    new_data = pd.DataFrame([[timestamp, drill, distance, attempts, made, percentage]], 
                            columns=["Timestamp", "Drill", "Distance_Ft", "Attempts", "Made", "Percentage"])
    
    # Append to CSV
    new_data.to_csv(DATA_FILE, mode='a', header=False, index=False)
    st.success(f"Logged! You shot {percentage:.1f}% from {distance} feet.")

# 3. Quick Data View
st.subheader("Your Recent Rounds")
df_display = pd.read_csv(DATA_FILE)
st.dataframe(df_display.tail(5)) # Shows last 5 rounds
