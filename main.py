from flask import Flask, render_template, request
import os
import re
import PyPDF2
import docx2txt
from werkzeug.utils import secure_filename
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"

if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])

SKILLS = [
    "python", "java", "c++", "html", "css", "javascript",
    "react", "node", "express", "flask", "django",
    "sql", "mysql", "mongodb", "postgresql",
    "machine learning", "deep learning", "nlp", "ai",
    "pandas", "numpy", "scikit-learn", "tensorflow", "keras",
    "pytorch", "data analysis", "power bi", "tableau",
    "git", "github", "docker", "aws", "azure",
    "rest api", "api", "linux", "oops", "dbms"
]

EDUCATION_KEYWORDS = [
    "b.tech", "bachelor", "computer science", "engineering",
    "m.tech", "masters", "degree", "university", "college"
]


def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def extract_text_from_docx(file_path):
    return docx2txt.process(file_path)


def extract_text_from_txt(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        return file.read()


def extract_text(file_path):
    lower_path = file_path.lower()

    if lower_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif lower_path.endswith(".docx"):
        return extract_text_from_docx(file_path)
    elif lower_path.endswith(".txt"):
        return extract_text_from_txt(file_path)
    return ""


def extract_email(text):
    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    match = re.search(pattern, text)
    return match.group() if match else "Not Found"


def extract_phone(text):
    pattern = r"(\+91[-\s]?)?[6-9]\d{9}"
    match = re.search(pattern, text)
    return match.group() if match else "Not Found"


def extract_name(text):
    lines = text.split('\n')

    for line in lines[:10]:

        line = line.strip()

        if not line:
            continue

        # skip email line
        if '@' in line:
            continue

        # skip phone line
        if any(ch.isdigit() for ch in line):
            continue

        words = line.split()

        # Name usually 1-3 words
        if 1 <= len(words) <= 3:

            # avoid section headings
            blacklist = [
                "education",
                "skills",
                "experience",
                "projects",
                "summary",
                "objective",
                "resume"
            ]

            if line.lower() not in blacklist:
                return line.title()

    return "Not Found"


def extract_skills(text):
    text = text.lower()
    found_skills = []

    for skill in SKILLS:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
            found_skills.append(skill)

    return sorted(list(set(found_skills)))


def calculate_format_score(text):
    score = 0
    text_lower = text.lower()

    if extract_email(text) != "Not Found":
        score += 2
    if extract_phone(text) != "Not Found":
        score += 2
    if "education" in text_lower:
        score += 2
    if "skills" in text_lower:
        score += 2
    if "project" in text_lower or "experience" in text_lower:
        score += 2

    return score


def calculate_ats_score(resume_text, job_description):
    resume_text_lower = resume_text.lower()
    jd_lower = job_description.lower()

    jd_skills = [skill for skill in SKILLS if skill in jd_lower]
    resume_skills = extract_skills(resume_text)

    matched_skills = sorted(list(set(jd_skills) & set(resume_skills)))
    missing_skills = sorted(list(set(jd_skills) - set(resume_skills)))

    if jd_skills:
        skill_score = (len(matched_skills) / len(jd_skills)) * 40
    else:
        skill_score = 20

    education_match = any(keyword in resume_text_lower for keyword in EDUCATION_KEYWORDS)
    education_score = 15 if education_match else 5

    experience_match = (
        "experience" in resume_text_lower
        or "internship" in resume_text_lower
        or "project" in resume_text_lower
        or "worked" in resume_text_lower
    )
    experience_score = 20 if experience_match else 8

    jd_words = set(jd_lower.split())
    resume_words = set(resume_text_lower.split())
    common_words = jd_words.intersection(resume_words)
    keyword_score = min((len(common_words) / max(len(jd_words), 1)) * 15, 15)

    formatting_score = calculate_format_score(resume_text)

    total_score = min(
        skill_score + education_score + experience_score + keyword_score + formatting_score,
        100
    )

    return round(total_score, 2), matched_skills, missing_skills


def generate_suggestions(missing_skills, ats_score, resume_text):
    suggestions = []

    if missing_skills:
        suggestions.append("Add important missing skills: " + ", ".join(missing_skills[:5]))

    if ats_score < 70:
        suggestions.append("Improve keyword alignment with the job description.")

    if "project" not in resume_text.lower():
        suggestions.append("Add a project section with technologies used and measurable results.")

    if "github" not in resume_text.lower():
        suggestions.append("Add GitHub or portfolio link.")

    if not re.search(r"\d+%|\d+\+", resume_text):
        suggestions.append("Add measurable achievements like accuracy, percentage improvement, or number of users.")

    if not suggestions:
        suggestions.append("Resume is well aligned with the job description.")

    return suggestions


def generate_summary(ats_score):
    if ats_score >= 80:
        return "Strong candidate with excellent skill alignment."
    elif ats_score >= 60:
        return "Good candidate with moderate alignment."
    elif ats_score >= 40:
        return "Average candidate with noticeable skill gaps."
    return "Low alignment with current job requirements."


def get_ats_category(ats_score):
    if ats_score >= 80:
        return "Excellent"
    elif ats_score >= 60:
        return "Good"
    elif ats_score >= 40:
        return "Average"
    return "Poor"


@app.route("/")
def home():
    return render_template("match_resume.html")


@app.route("/matcher", methods=["GET", "POST"])
def matcher():
    if request.method == "POST":
        job_description = request.form.get("job_description")
        resume_files = request.files.getlist("resumes")

        if not job_description or not resume_files:
            return render_template(
                "match_resume.html",
                message="Please upload resumes and enter a job description."
            )

        resume_texts = []
        file_names = []

        for resume_file in resume_files:
            if resume_file.filename == "":
                continue

            filename = secure_filename(resume_file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            resume_file.save(file_path)

            text = extract_text(file_path)

            if text.strip():
                resume_texts.append(text)
                file_names.append(filename)

        if not resume_texts:
            return render_template(
                "match_resume.html",
                message="No readable resume text found."
            )

        vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_matrix = vectorizer.fit_transform([job_description] + resume_texts)

        job_vector = tfidf_matrix[0]
        resume_vectors = tfidf_matrix[1:]
        similarities = cosine_similarity(job_vector, resume_vectors)[0]

        results = []

        for i, resume_text in enumerate(resume_texts):
            ats_score, matched_skills, missing_skills = calculate_ats_score(
                resume_text,
                job_description
            )

            candidate_name = extract_name(resume_text)

            if candidate_name == "Not Found":
                candidate_name = file_names[i] \
                    .replace(".pdf", "") \
                    .replace(".docx", "") \
                    .replace(".txt", "") \
                    .replace("_", " ") \
                    .replace("-", " ") \
                    .title()

            similarity_score = round(similarities[i] * 100, 2)

            candidate = {
                "filename": file_names[i],
                "name": candidate_name,
                "email": extract_email(resume_text),
                "phone": extract_phone(resume_text),
                "similarity_score": similarity_score,
                "ats_score": ats_score,
                "ats_category": get_ats_category(ats_score),
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
                "summary": generate_summary(ats_score),
                "suggestions": generate_suggestions(missing_skills, ats_score, resume_text),
                "final_score": round((ats_score * 0.7) + (similarity_score * 0.3), 2)
            }

            results.append(candidate)

        results = sorted(results, key=lambda x: x["final_score"], reverse=True)

        total_resumes = len(results)
        average_score = round(sum(r["ats_score"] for r in results) / total_resumes, 2)
        best_candidate = results[0]["filename"]

        return render_template(
            "match_resume.html",
            message="Resume matching completed successfully.",
            results=results,
            total_resumes=total_resumes,
            average_score=average_score,
            best_candidate=best_candidate
        )

    return render_template("match_resume.html")


if __name__ == "__main__":
    app.run(debug=True)