# HireSense AI - Intelligent ATS & Resume Screening Platform

## Overview

HireSense AI is an AI-powered Applicant Tracking System (ATS) and Resume Screening Platform designed to automate candidate shortlisting. The system analyzes resumes against a given job description, calculates ATS scores, identifies skill gaps, ranks candidates, and provides actionable recruiter insights.

Unlike traditional keyword-based resume screening tools, HireSense AI evaluates resumes using multiple parameters including skill alignment, education, experience, keyword coverage, formatting quality, and NLP-based similarity analysis.

---
## Live Demo 
https://hiresense-ai-1-seqd.onrender.com/matcher

---
## Features

### Resume Parsing

- Name Extraction
- Email Extraction
- Phone Number Extraction

### ATS Score Calculation

Calculates ATS Score out of 100 based on:

- Skill Match
- Education Match
- Experience Match
- Keyword Coverage
- Resume Formatting

### Resume Ranking

Ranks candidates using:

- 70% ATS Score
- 30% Similarity Score

### NLP-Based Matching

Uses:

- TF-IDF Vectorization
- Cosine Similarity

### Skill Gap Analysis

#### Matched Skills

Skills found in both Job Description and Resume.

#### Missing Skills

Skills required by the Job Description but absent from the Resume.

### Resume Improvement Suggestions

Provides recommendations such as:

- Missing Skills
- GitHub Portfolio Missing
- Missing Project Section
- Weak Keyword Alignment
- Lack of Measurable Achievements

### Candidate Summary

Generates recruiter-friendly summaries:

- Excellent Candidate
- Good Candidate
- Average Candidate
- Low Alignment Candidate

### Recruiter Dashboard

Displays:

- Total Resumes Uploaded
- Average ATS Score
- Best Candidate
- Ranked Candidates

---

## Project Architecture

```text
Job Description
       |
       v
Resume Upload
       |
       v
Text Extraction
(PDF / DOCX / TXT)
       |
       v
Resume Parsing
(Name, Email, Phone)
       |
       v
Skill Extraction
       |
       v
ATS Score Calculation
       |
       v
TF-IDF Vectorization
       |
       v
Cosine Similarity
       |
       v
Final Ranking Engine
       |
       v
Candidate Insights Dashboard
```

---

## Tech Stack

### Backend

- Python
- Flask

### NLP & Machine Learning

- Scikit-learn
- TF-IDF Vectorizer
- Cosine Similarity

### Resume Processing

- PyPDF2
- docx2txt

### Frontend

- HTML5
- CSS3
- Bootstrap 4
- Jinja2

---

## Project Structure

```text
HIRESENSEAI/
│
├── main.py
├── requirements.txt
├── README.md
│
├── uploads/
│
├── templates/
│   └── match_resume.html

```

---

## ATS Scoring Methodology

### Skill Match (40%)

Measures overlap between:

- Required Skills
- Resume Skills

### Education Match (15%)

Checks:

- Bachelor's Degree
- Engineering Degree
- Computer Science Background

### Experience Match (20%)

Checks:

- Internship Experience
- Project Experience
- Professional Experience

### Keyword Coverage (15%)

Measures keyword overlap between:

- Job Description
- Resume

### Resume Formatting (10%)

Checks:

- Email
- Phone Number
- Skills Section
- Education Section
- Projects/Experience Section

---

## Candidate Ranking Formula

```python
final_score = (
    ats_score * 0.7 +
    similarity_score * 0.3
)
```

---

## Supported File Formats

- PDF (.pdf)
- DOCX (.docx)
- TXT (.txt)

---

## Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/hiresense-ai.git
cd hiresense-ai
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Environment

#### Windows

```bash
.venv\Scripts\activate
```

#### Linux / Mac

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
python main.py
```

### Open Browser

```text
http://127.0.0.1:5000
```

---

## Workflow

### Step 1

Paste a Job Description

### Step 2

Upload Multiple Resumes

### Step 3

System Performs:

- Resume Parsing
- ATS Scoring
- Skill Extraction
- Similarity Analysis
- Candidate Ranking

### Step 4

View:

- ATS Score
- Similarity Score
- Final Rank Score
- Candidate Summary
- Matched Skills
- Missing Skills
- Resume Suggestions

---

## Current Limitations

- Uses TF-IDF instead of semantic embeddings
- Does not support scanned PDFs
- No database integration
- Single-user architecture

---

## Future Enhancements

### Semantic Search

Replace TF-IDF with:

- Sentence Transformers
- BERT Embeddings

### Vector Search

Integrate:

- FAISS
- Pinecone
- Qdrant

### OCR Support

Support scanned resumes using:

- Tesseract OCR
- EasyOCR

### Multi-User ATS

- Recruiter Login
- Candidate Database
- Job Management

### Cloud Database

- PostgreSQL
- MongoDB

### AI-Powered Resume Review

Generate:

- Resume Feedback
- ATS Optimization Tips
- Interview Readiness Analysis

### RAG-Based Candidate Search

Allow recruiters to search candidates using natural language queries and semantic retrieval.

----

## Author

**Ekta**

B.Tech Computer Science & Artificial Intelligence (CSAI)

Netaji Subhas University of Technology (NSUT)
