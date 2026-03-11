from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PyPDF2 import PdfReader
import os

app = Flask(__name__)
CORS(app)

# -------- Resume Text Extractor --------
def extract_resume_text(file):

    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()

    return text.lower()


# -------- Load Skills Dataset --------
def load_skills():

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    skills_path = os.path.join(base_dir, "dataset", "skills.txt")

    with open(skills_path) as f:
        skills = f.read().splitlines()

    return skills


# -------- Skill Extraction --------
def extract_skills(text, skills_list):

    found_skills = []

    for skill in skills_list:
        if skill in text:
            found_skills.append(skill)

    return found_skills


# -------- Resume Suggestions --------
def generate_suggestions(score):

    suggestions = []

    if score < 40:
        suggestions.append("Add more technical skills")
        suggestions.append("Include projects related to the role")
        suggestions.append("Improve resume keywords")

    elif score < 70:
        suggestions.append("Add measurable achievements")
        suggestions.append("Include more tools or frameworks")

    else:
        suggestions.append("Resume is strong for this role")

    return suggestions


# -------- Resume Section Detection --------
def detect_sections(text):

    sections = []

    keywords = {
        "Education":["education","degree","university","college"],
        "Projects":["project","projects"],
        "Skills":["skills","technical skills"],
        "Experience":["experience","internship","work experience"]
    }

    for section, words in keywords.items():
        for word in words:
            if word in text:
                sections.append(section)
                break

    return sections


# -------- Main Analyze API --------
@app.route("/analyze", methods=["POST"])
def analyze():

    resume_file = request.files["resume"]
    job_desc = request.form["jobdesc"].lower()

    resume_text = extract_resume_text(resume_file)

    skills_list = load_skills()

    resume_skills = extract_skills(resume_text, skills_list)
    job_skills = extract_skills(job_desc, skills_list)

    matched_skills = list(set(resume_skills) & set(job_skills))
    missing_skills = list(set(job_skills) - set(resume_skills))

    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([resume_text, job_desc])

    similarity = cosine_similarity(vectors)[0][1]
    similarity_score = similarity * 100

    # Skill score
    if len(job_skills) > 0:
        skill_score = (len(matched_skills) / len(job_skills)) * 100
    else:
        skill_score = 0

    sections = detect_sections(resume_text)

    section_score = (len(sections) / 4) * 100

    score = round((0.5 * similarity_score) + (0.3 * skill_score) + (0.2 * section_score), 2)

    # Final score
    score = round((0.5 * similarity_score) + (0.3 * skill_score) + (0.2 * section_score), 2)

    suggestions = generate_suggestions(score)

    return jsonify({
        "score": score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "suggestions": suggestions,
        "sections": sections,
        "skill_match": round(skill_score, 2)
    })

if __name__ == "__main__":
    app.run(debug=True)