import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# Function to load and analyze job data
def job_analysis():
    st.title("📊 Job Market Analysis Dashboard")

    # Load the extracted job data (Ensure jobs_data is available)
    if "jobs_data" not in st.session_state:
        st.warning("No job data available. Please extract job details first!")
        return

    df = pd.DataFrame(st.session_state.jobs_data)

    # --- Job Titles by Company ---
    st.subheader("🏢 Job Titles by Company")
    company_job_counts = df.groupby("Company Name")["Job Title"].count().sort_values(ascending=False)
    st.bar_chart(company_job_counts)

    # --- Most Common Job Titles ---
    st.subheader("🔥 Most Frequent Job Titles")
    all_job_titles = df["Job Title"].tolist()
    title_counts = Counter(all_job_titles)
    most_common_titles = title_counts.most_common(10)  # Top 10 job titles
    st.write(pd.DataFrame(most_common_titles, columns=["Job Title", "Count"]))

    # --- Job Titles by Location ---
    st.subheader("📍 Job Titles by Location")
    location_job_counts = df.groupby("Location")["Job Title"].count().sort_values(ascending=False)
    st.bar_chart(location_job_counts)

    # --- Job Distribution by Keyword ---
    st.subheader("🔍 Keyword-based Job Analysis")
    keywords = ["Computer Vision", "Gen AI", "NLP", "Testing"]
    keyword_counts = {kw: 0 for kw in keywords}

    for job in df["Job Title"]:
        for kw in keywords:
            if kw.lower() in job.lower():
                keyword_counts[kw] += 1

    # Sort keyword counts in descending order
    sorted_counts = dict(sorted(keyword_counts.items(), key=lambda item: item[1], reverse=True))

    # Plot with Seaborn for better aesthetics
    fig, ax = plt.subplots()
    sns.set_style("whitegrid")
    sns.barplot(x=list(sorted_counts.keys()), y=list(sorted_counts.values()), palette="Blues_d", ax=ax)

    # Add value labels above bars
    for i, val in enumerate(sorted_counts.values()):
        ax.text(i, val + 0.1, str(val), ha='center', va='bottom', fontsize=10)

    ax.set_xlabel("Keyword", fontsize=12)
    ax.set_ylabel("Number of Jobs", fontsize=12)
    ax.set_title("Jobs Matching Specific Keywords", fontsize=14)
    plt.xticks(rotation=15)
    st.pyplot(fig)

# Run the function when the page is selected
job_analysis()
