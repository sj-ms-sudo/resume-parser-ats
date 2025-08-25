# 📄 Resume Parser & ATS (Flask)

A Flask-based Resume Parser and Applicant Tracking System (ATS) that analyzes resumes, extracts candidate details, matches skills, and computes ATS scores.

## 🚀 Features
- Resume Parsing (PDF, spaCy, regex)
- ATS Skill Matching & Scoring
- Admin Dashboard
- Skill Management
- ATS Score Visualization (D3.js)

## 🗂 Project Structure
(Insert tree structure here)

## ⚡ Setup
```bash
git clone https://github.com/yourusername/resume-parser-ats.git
cd resume-parser-ats
pip install -r requirements.txt
python -m spacy download en_core_web_md
python db.py
python skilldb.py
python user.py
python app.py
