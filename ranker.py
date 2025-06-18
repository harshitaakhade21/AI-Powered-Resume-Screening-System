def match_score(resume_data, job_description):
    score = 0
    jd_lower = job_description.lower()

    for skill in resume_data["skills"]:
        if skill.lower() in jd_lower:
            score += 10

    for edu in resume_data["education"]:
        if edu.lower() in jd_lower:
            score += 5

    for exp in resume_data["experience"]:
        score += 5  # Simple score for experience mention

    return score

import spacy

nlp = spacy.load("en_core_web_md")

def match_score(data, jd_text):
    jd_doc = nlp(jd_text.lower())
    combined_resume_text = " ".join(data["skills"] + data["education"] + data["experience"])
    resume_doc = nlp(combined_resume_text.lower())
    return jd_doc.similarity(resume_doc)  # Returns float between 0 and 1

