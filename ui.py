import streamlit as st
import os
from app import generate_resume  # Import the generate_resume function

def main():
    st.title("Resume Generator")

    # Define a form for user inputs
    with st.form("resume_form"):
        name = st.text_input("Enter your name")
        phone = st.text_input("Enter your phone number")
        email = st.text_input("Enter your email")
        education = st.text_area("Enter your education details (separate entries with a newline)").split('\n')
        skills = st.text_area("Enter your skills (separate skills with a newline)").split('\n')
        hobbies = st.text_area("Enter your hobbies (separate hobbies with a newline)").split('\n')
        summary = st.text_area("Enter a professional summary or type 'generate' to create one")
        experience = st.text_area("Enter your professional experience (separate experiences with a newline)").split('\n')
        certifications = st.text_area("Enter your certifications (separate certifications with a newline)").split('\n')
        languages = st.text_area("Enter languages you speak (separate languages with a newline)").split('\n')
        publications = st.text_area("Enter your publications (separate publications with a newline)").split('\n')
        references = st.text_area("Enter your references (separate references with a newline)").split('\n')

        submit_button = st.form_submit_button(label="Generate Resume")

    if submit_button:
        user_info = {
            "name": name,
            "phone": phone,
            "email": email,
            "education": education,
            "skills": skills,
            "hobbies": hobbies,
            "summary": summary,
            "experience": experience,
            "certifications": certifications,
            "languages": languages,
            "publications": publications,
            "references": references,
        }
        
        resume_path = generate_resume(user_info)
        # Provide the resume as a downloadable file
        with open(resume_path, "rb") as file:
            st.download_button(
                label="Download Resume",
                data=file,
                file_name=os.path.basename(resume_path),
                mime="application/pdf"
            )

if __name__ == "__main__":
    main()
