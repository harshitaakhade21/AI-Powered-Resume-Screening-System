from ctypes import c_buffer
import streamlit as st
import os
from parser import extract_text_from_pdf, extract_info
from ranker import match_score
from database import create_db, insert_resume
import sqlite3
import pandas as pd


st.set_page_config(page_title="AI Resume Screener", layout="wide")

st.title("AI-Powered Resume Screening System")

create_db()

# ============================
# Job Description Section
# ============================
st.markdown("### Job Description")
jd_input = st.text_area("Paste the job description here:", height=200)

st.markdown("---")

# ============================
# Resume Upload Section
# ============================
st.markdown("### Upload Resumes")
uploaded_files = st.file_uploader("Upload one or more resumes (PDF)", type="pdf", accept_multiple_files=True)

st.markdown("---")


if st.button("🔍 Analyze Resumes"):
    st.markdown("#### Processing resumes... Please wait ⏳")

    if jd_input.strip() == "":
        st.error("Please paste a job description first.")
    elif not uploaded_files:
        st.error("Please upload at least one resume.")
    else:
        st.success("Processing resumes...")
        results = []
        for uploaded_file in uploaded_files:
            with open(uploaded_file.name, "wb") as f:
                f.write(uploaded_file.read())

            text = extract_text_from_pdf(uploaded_file.name)
            data = extract_info(text)
            score = round(match_score(data, jd_input) * 100, 2)
            insert_resume(uploaded_file.name, data, score)

            results.append((uploaded_file.name, score, data))
            os.remove(uploaded_file.name)

        # Show Results and Add CSV Download
        st.subheader("Resume Rankings")
        sorted_results = sorted(results, key=lambda x: x[1], reverse=True)
        for name, score, data in sorted_results:
            with st.expander(f"{name} — Score: {score}"):
                st.write("**Skills:**", ", ".join(data["skills"]))
                st.write("**Education:**", ", ".join(data["education"]))
                st.write("**Experience:**", ", ".join(data["experience"]))

        # Convert to CSV
        df = pd.DataFrame([{
            "Name": name,
            "Score": score,
            "Skills": ", ".join(data["skills"]),
            "Education": ", ".join(data["education"]),
            "Experience": ", ".join(data["experience"])
        } for name, score, data in sorted_results])

        st.subheader("Download Results")
        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download CSV of Ranked Resumes",
            data=csv,
            file_name="ranked_resumes.csv",
            mime="text/csv",
        )
