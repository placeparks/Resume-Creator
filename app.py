import openai
import os
from dotenv import load_dotenv
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib import colors
# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Function to collect user information
def collect_user_info():
    user_info = {
        "name": input("Enter your name: "),
        "phone": input("Enter your phone number: "),
        "email": input("Enter your email: "),
        "education": [],
        "skills": [],
        "hobbies": [],
        "summary": input("Enter a professional summary (or type 'generate' to create one): "),
        "experience": [],
        "certifications": [],
        "languages": [],
        "publications": [],
        "references": [],
    }
    
    # Collect multiple entries for various sections
    sections = ["education", "skills", "hobbies", "experience", "certifications", "languages", "publications", "references"]
    for section in sections:
        while True:
            entry = input(f"Enter your {section} (or type 'done' to finish): ")
            if entry.lower() == 'done':
                break
            user_info[section].append(entry)

    return user_info


# Function to format the resume with ReportLab
def format_resume(user_info):
    doc = SimpleDocTemplate("resume.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    custom_style = ParagraphStyle('CustomStyle', parent=styles['Normal'], alignment=TA_LEFT, textColor=colors.darkblue)
    heading_style = styles['Heading2']
    normal_style = styles['Normal']
    story = []

    # Convert name to uppercase and add contact information
    story.append(Paragraph(user_info['name'].upper(), styles['Title']))
    story.append(Paragraph(f"<b>Contact:</b> {user_info['phone']}", custom_style))
    story.append(Paragraph(f"<b>Email:</b> {user_info['email']}", custom_style))
    story.append(Spacer(1, 12))

    # Professional summary
    story.append(Paragraph("<b>Professional Summary</b>", heading_style))
    story.append(Paragraph(user_info['summary'], normal_style))
    story.append(Spacer(1, 12))

    # Section formatting with conditional check
    for section, title in [
        ('education', 'Education'),
        ('skills', 'Skills'),
        ('hobbies', 'Hobbies'),
        ('experience', 'Professional Experience'),
        ('publications', 'Publications'),
       ('languages', 'Languages'),
       ('certifications', 'Certifications'),
    ]:
        content = user_info.get(section, [])
        if any(content):  # Check if the section has content (not just empty strings)
            story.append(Paragraph(f"<b>{title}</b>", heading_style))
            for item in content:
                if item.strip():  # Check if the item is not just white space
                    story.append(Paragraph(item, styles['Bullet']))
            story.append(Spacer(1, 12))

    return story


def refine_data_with_openai(user_info):
  # If 'generate' was chosen, use OpenAI to create a professional summary
    if user_info['summary'].lower() == 'generate':
        summary_prompt = f"Create a professional summary based on the following skills: {', '.join(user_info['skills'])}."
        
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=summary_prompt,
            temperature=0.5,
            max_tokens=1000  # Increased the max_tokens value
        )
        
        user_info['summary'] = response.choices[0].text.strip()
    return user_info

def generate_resume(user_info):
    # If summary needs to be generated
    if user_info['summary'].lower() == 'generate':
        user_info = refine_data_with_openai(user_info)

    # Format the resume and build the PDF
    story = format_resume(user_info)
    doc = SimpleDocTemplate("resume.pdf", pagesize=letter)
    doc.build(story)

    return "resume.pdf"

# The main function can be used for testing or standalone execution
def main():
    user_info = collect_user_info()
    pdf_path = generate_resume(user_info)
    print(f"Resume generated successfully as {pdf_path}")


if __name__ == "__main__":
    main()
