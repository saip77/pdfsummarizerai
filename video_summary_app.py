import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from PyPDF2 import PdfReader

# Load environment variables
load_dotenv()

# Configure API key
api_key = os.getenv("GOOGLE_API_KEY")
if api_key is None:
    st.error("API key not found. Please set the GOOGLE_API_KEY environment variable.")
else:
    genai.configure(api_key=api_key)

# Prompt logic
prompt = """
You are a PDF summarizer. You will take the text from the PDF, summarize it in 60 words.
"""

# Function to extract text from PDF
def extract_pdf_text(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to generate summary and FAQs using Google Gemini API
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")  # Example of using Google's model
    response = model.generate_content(prompt + transcript_text)
    return response.text

st.title("PDF Summarizer")

# File uploader for PDFs
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    pdf_text = extract_pdf_text(uploaded_file)

    if pdf_text:
        # Generate summary and FAQs using Google Gemini
        summary_and_faqs = generate_gemini_content(pdf_text, prompt)

        # Display the results
        st.markdown("## Summary:")
        st.write(summary_and_faqs)