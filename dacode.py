import streamlit as st
import pandas as pd
import re
import cv2
import requests
from datetime import datetime

# Custom CSS for styling
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    color: #333;
}

.logo {
    position: absolute;
    top: 10px;
    left: 10px;
    width: 100px;
}

.stButton>button {
    background-color: #4CAF50;
    color: white;
    padding: 10px 24px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.stButton>button:hover {
    background-color: #45a049;
}

.clt-color {
    background-color: #FF5733;
    color: white;
    padding: 10px;
    border-radius: 5px;
}

.cfc-color {
    background-color: #33FF57;
    color: white;
    padding: 10px;
    border-radius: 5px;
}

.iipc-color {
    background-color: #3357FF;
    color: white;
    padding: 10px;
    border-radius: 5px;
}

.sri-color {
    background-color: #F033FF;
    color: white;
    padding: 10px;
    border-radius: 5px;
}
</style>
""", unsafe_allow_html=True)

# Function to create a simple logo
def create_logo():
    logo_image = """
    <svg height="100" width="100">
        <circle cx="50" cy="50" r="40" stroke="black" stroke-width="3" fill="#4CAF50" />
        <text fill="white" font-family="Arial" font-size="20" x="30" y="60">SNS</text>
    </svg>
    """
    return logo_image

# Display the logo
st.markdown(create_logo(), unsafe_allow_html=True)

# Initialize session state for tracking submissions
if 'submissions' not in st.session_state:
    st.session_state.submissions = {}

# Function to analyze video duration
def analyze_video_duration(video_url):
    try:
        cap = cv2.VideoCapture(video_url)
        if not cap.isOpened():
            return "Error: Could not open video."
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps
        return duration
    except Exception as e:
        return f"Error: {str(e)}"

# Function to verify LinkedIn article
def verify_linkedin_article(article_url):
    try:
        response = requests.get(article_url)
        if response.status_code == 200:
            content = response.text
            word_count = len(re.findall(r'\w+', content))
            hashtags = ['#snsinstitution', '#designthinking', '#snsdesignthinkers']
            contains_hashtags = all(hashtag in content for hashtag in hashtags)
            return word_count >= 250 and contains_hashtags
        else:
            return False
    except Exception as e:
        return f"Error: {str(e)}"

# Function to submit task for a pillar
def submit_task(pillar, task_details):
    st.session_state.submissions[pillar] = {
        "task_details": task_details,
        "submission_date": datetime.now().strftime("%Y-%m-%d")
    }

# CLT Pillar Form
with st.expander("CLT Pillar", expanded=True):
    st.markdown("<p class='clt-color'>CLT Pillar</p>", unsafe_allow_html=True)
    with st.form(key='clt_form'):
        clt_task_details = st.text_area("Task Details for CLT")
        video_urls = st.text_area("Enter YouTube Video URLs (one per line)")

        if st.form_submit_button("Submit CLT"):
            if not clt_task_details or not video_urls:
                st.error("Please fill in all the details.")
            else:
                video_urls_list = video_urls.split('\n')
                for url in video_urls_list:
                    duration = analyze_video_duration(url)
                    st.write(f"Video Duration: {duration} seconds")
                submit_task("CLT", clt_task_details)
                st.success("Task for CLT submitted successfully!")

# CFC Pillar Form
with st.expander("CFC Pillar", expanded=True):
    st.markdown("<p class='cfc-color'>CFC Pillar</p>", unsafe_allow_html=True)
    with st.form(key='cfc_form'):
        cfc_task_details = st.text_area("Task Details for CFC")
        patent_details = st.text_area("Patent Details")
        journal_details = st.text_area("Journal Details")

        if st.form_submit_button("Submit CFC"):
            if not cfc_task_details or not patent_details or not journal_details:
                st.error("Please fill in all the details.")
            else:
                submit_task("CFC", cfc_task_details)
                st.success("Task for CFC submitted successfully!")

# IIPC Pillar Form
with st.expander("IIPC Pillar", expanded=True):
    st.markdown("<p class='iipc-color'>IIPC Pillar</p>", unsafe_allow_html=True)
    with st.form(key='iipc_form'):
        iipc_task_details = st.text_area("Task Details for IIPC")
        article_urls = st.text_area("LinkedIn Article URLs (one per line)")

        if st.form_submit_button("Submit IIPC"):
            if not iipc_task_details or not article_urls:
                st.error("Please fill in all the details.")
            else:
                article_urls_list = article_urls.split('\n')
                for url in article_urls_list:
                    is_valid = verify_linkedin_article(url)
                    st.write(f"Article Verification: {'Valid' if is_valid else 'Invalid'}")
                submit_task("IIPC", iipc_task_details)
                st.success("Task for IIPC submitted successfully!")

# SRI Pillar Form
with st.expander("SRI Pillar", expanded=True):
    st.markdown("<p class='sri-color'>SRI Pillar</p>", unsafe_allow_html=True)
    with st.form(key='sri_form'):
        sri_task_details = st.text_area("Task Details for SRI")
        excel_file = st.file_uploader("Upload Excel Sheet", type=["xlsx", "xls"])

        if st.form_submit_button("Submit SRI"):
            if not sri_task_details or excel_file is None:
                st.error("Please fill in all the details.")
            else:
                submit_task("SRI", sri_task_details)
                st.success("Task for SRI submitted successfully!")

# Generate a faculty report if all pillars are submitted
if len(st.session_state.submissions) == 4:
    report_data = []
    for pillar, details in st.session_state.submissions.items():
        report_data.append({
            "Pillar Name": pillar,
            "Task Details": details["task_details"],
            "Submission Date": details["submission_date"]
        })

    report_df = pd.DataFrame(report_data)

    # Display the report
    st.subheader("Faculty Report")
    st.dataframe(report_df)

    # Download the report as CSV
    st.download_button(
        label="Download Faculty Report",
        data=report_df.to_csv(index=False).encode('utf-8'),
        file_name='faculty_report.csv',
        mime='text/csv',
    )
