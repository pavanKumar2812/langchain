import streamlit as st
from extract_job_details_linkedin import extract_job_details
import pandas as pd
from utils import show_signature

show_signature()

# Title
st.title("💼 Job Data Extraction & Analysis")

# Initialize session state
if "jobs_data" not in st.session_state:
    st.session_state.jobs_data = None

# User input for LinkedIn URL
url = st.text_input("Enter LinkedIn Job Search URL:")

# Only extract new data if a URL is entered
if url:
    try:
        jobs_data = extract_job_details(url)
        st.session_state.jobs_data = jobs_data  # Save to session state
        st.success("✅ Job data extracted successfully.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Display job data if available
if st.session_state.jobs_data:
    df = pd.DataFrame(st.session_state.jobs_data)

    # Convert "Company Link" column into clickable hyperlinks
    if "Company Link" in df.columns:
        df["Company Link"] = df["Company Link"].apply(lambda x: f'<a href="{x}" target="_blank">🔗 Click Here</a>')

    # Display DataFrame
    st.markdown(df.to_html(escape=False), unsafe_allow_html=True)