import streamlit as st
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import HuggingFaceEndpoint
from fpdf import FPDF

# Load API key from .env
load_dotenv()
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACE_API_KEY")
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN

# LLM setup
repo_id = "mistralai/Mistral-7B-Instruct-v0.2"
llm = HuggingFaceEndpoint(
    repo_id=repo_id,
    max_length=512,
    temperature=0.7,
    token=HUGGINGFACEHUB_API_TOKEN,
    task="text-generation"
)

# Prompt setup
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a professional resume and cover letter generator."),
    ("user", "{user_input}")
])

# PDF Generator
def generate_pdf(text, filename="generated_resume.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in text.split('\n'):
        pdf.multi_cell(0, 10, line)
    pdf.output(filename)

# Streamlit UI
st.set_page_config(page_title="LLM Resume Builder", layout="centered")
st.title("🤖 LLM Resume or Cover Letter Generator")
st.markdown("Fill in the details below and get your professional PDF instantly!")

# Initialize session_state
if "user_details" not in st.session_state:
    st.session_state.user_details = ""
if "job_description" not in st.session_state:
    st.session_state.job_description = ""
if "response" not in st.session_state:
    st.session_state.response = ""

with st.form("user_input_form"):
    user_details = st.text_area("✍️ Your Profile (name, skills, experience, education, etc.):",
                                value=st.session_state.user_details,
                                height=150)
    job_description = st.text_area("💼 Job Description / Target Role:",
                                   value=st.session_state.job_description,
                                   height=150)
    submit_button = st.form_submit_button("Generate Resume or Cover Letter")

if submit_button:
    st.session_state.user_details = user_details
    st.session_state.job_description = job_description

    with st.spinner("Generating with LLM..."):
        final_prompt = f"""I want you to generate a professional resume for the following person.
                            Details:
                            Name: {user_details.strip()}
                            Applying for: {job_description.strip()}

                            Please create the resume in this format:
                            1. Name & Contact Info (with placeholders for phone and email)
                            2. Professional Summary
                            3. Skills
                            4. Experience
                            5. Projects
                            6. Education
                            7. Certifications
                            8. Soft Skills

                            Be concise and professional."""

        response = llm.invoke(final_prompt)

        st.session_state.response = response  # Save in session state

        generate_pdf(response)
        st.success("🎉 Resume/Cover Letter generated!")

if st.session_state.response:
    st.subheader("📄 Preview:")
    st.text_area("Generated Text:", value=st.session_state.response, height=300)

    with open("generated_resume.pdf", "rb") as f:
        st.download_button("📥 Download PDF", f, file_name="resume.pdf")
