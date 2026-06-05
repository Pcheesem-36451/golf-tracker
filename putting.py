import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.request
import urllib.parse

# 1. Page Configuration
st.set_page_config(page_title="Golf Putting Tracker", page_icon="⛳", layout="centered")

# 2. Header and Tableau Link
st.title("⛳ Putting Stats Tracker")
st.markdown("### 📊 [View My Tableau Dashboard](https://public.tableau.com/views/PhilPuttingPractice/Dashboard1?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)")
st.write("Log your practice sessions directly into Google Sheets.")
st.write("---")

# --- CONFIGURATION (REPLACE WITH YOUR GOOGLE FORM DETAILS) ---
FORM_ID = "1FAIpQLSeZ1tu5PrBhg0k79vqpop7Fd8G5Sey3Gxo-KP7pnKLHWiobkg"
ENTRY_DRILL = "entry.1609274925"       # Replace with your actual entry IDs
ENTRY_DISTANCE = "entry.11254052"
ENTRY_ATTEMPTS = "entry.735277921"
ENTRY_MADE = "entry.2033739861"
ENTRY_PERCENTAGE = "entry.811923202"
# --------------------------------------------------------------
# 3. Input Fields
drill = st.selectbox("Select Drill", ["6-Foot Gauge", "Ladder Drill", "Around the World", "Random Practice"])
distance = st.number_input("Distance (Feet)", min_value=1, max_value=100, value=6)
attempts = st.number_input("Balls Attempted", min_value=1, value=4)
made = st.number_input("Balls Made", min_value=0, max_value=int(attempts), value=0)

# 4. Submission Logic
if st.button("Log Round to Cloud", use_container_width=True):
    percentage = (made / attempts) * 100
    
    # Formulate the payload to mirror a web form submission
    form_url = f"https://docs.google.com/forms/d/e/{FORM_ID}/formResponse"
    form_data = {
        ENTRY_DRILL: drill,
        ENTRY_DISTANCE: distance,
        ENTRY_ATTEMPTS: attempts,
        ENTRY_MADE: made,
        ENTRY_PERCENTAGE: f"{percentage:.1f}"
    }
    
    try:
        # Encode data and send via standard HTTP POST request
        encoded_data = urllib.parse.urlencode(form_data).encode("utf-8")
        request = urllib.request.Request(form_url, data=encoded_data)
        
        with urllib.request.urlopen(request) as response:
            if response.status == 200:
                st.success(f"🚀 Sent to Google Sheets! Shot {percentage:.1f}% from {distance} feet.")
            else:
                st.error("Form rejected the entry submission.")
    except Exception as e:
        st.error(f"Error connecting to Google: {e}")
