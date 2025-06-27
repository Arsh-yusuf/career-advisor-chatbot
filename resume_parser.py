# resume_parser.py
import fitz  # PyMuPDF

def extract_resume_data(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()

    text = text.lower()

    def extract_section(keyword, max_chars=500):
        idx = text.find(keyword)
        if idx != -1:
            return text[idx:idx + max_chars].replace('\n', ' ')
        return ""

    education = extract_section("education")
    skills = extract_section("skills")
    interests = extract_section("interests")

    return {
        "education": education.strip(),
        "skills": skills.strip(),
        "interests": interests.strip()
    }
