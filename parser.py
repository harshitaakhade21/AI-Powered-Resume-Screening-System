import re
import PyPDF2

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_info(text):
    skills = re.findall(r'\b(?:Python|Java|C\+\+|SQL|Machine Learning|Deep Learning|NLP|Data Analysis|Communication|Leadership)\b', text, re.I)
    education = re.findall(r'(B\.?Tech|M\.?Tech|B\.?E|M\.?E|Bachelor|Master)[^.,\n]*', text, re.I)
    experience = re.findall(r'(\d+)\+?\s+(?:years?|yrs?)\s+of\s+(?:experience|exp)', text, re.I)
    
    return {
        "skills": list(set([s.strip() for s in skills])),
        "education": list(set(education)),
        "experience": list(set(experience))
    }

def parse_job_description(jd_text):
    return jd_text
