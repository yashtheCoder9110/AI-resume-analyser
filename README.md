# AI-Powered Resume Screening & Job-Matching System

A Flask web app that reads resumes (PDF/DOCX/TXT), extracts skills using a
keyword-based matcher, compares them against a job description using both
**skill overlap** and **TF-IDF cosine similarity**, and ranks candidates by
match score — a simplified version of how real ATS (Applicant Tracking
Systems) work.

## Features
- Upload multiple resumes at once (PDF, DOCX, TXT)
- Paste any job description
- Automatic skill extraction from a 150+ keyword tech skills database
  (`skills_data.py` — easy to extend)
- Match score = weighted combination of:
  - Skill overlap score (65%)
  - TF-IDF text similarity score (35%)
- Ranked results with matched / missing / extra skills clearly shown
- Simple, clean Bootstrap UI, no frontend build step needed

## Tech Stack
- **Backend:** Python, Flask
- **NLP/ML:** scikit-learn (TF-IDF + cosine similarity), keyword-based skill extraction
- **File parsing:** pdfplumber (PDF), python-docx (DOCX)
- **Frontend:** HTML, Bootstrap 5 (via CDN)

## Setup & Run

1. Create a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate      # on Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   python app.py
   ```

4. Open your browser at:
   ```
   http://127.0.0.1:5000
   ```

## Project Structure
```
resume_matcher/
├── app.py              # Flask routes (/,  /match)
├── utils.py             # text extraction, skill extraction, scoring logic
├── skills_data.py        # master skills keyword database
├── requirements.txt
├── templates/
│   ├── index.html        # upload form
│   └── results.html       # ranked results page
├── static/
│   └── style.css
└── uploads/              # (unused at runtime, kept for future extension)
```

## How the Matching Works
1. **Text extraction:** the resume file is parsed into raw text.
2. **Skill extraction:** both the resume text and job description are
   scanned against `SKILLS_DB` using word-boundary regex matching so
   short skills like "R" or "C" don't false-match inside other words.
3. **Skill overlap score:** `matched skills / required skills` (from the JD).
4. **Text similarity score:** TF-IDF vectors of the JD and resume, compared
   with cosine similarity — this catches relevant context beyond the fixed
   skill list (e.g. phrasing, project descriptions).
5. **Final score:** `0.65 × skill_score + 0.35 × text_score`, shown as a
   percentage, with candidates ranked highest to lowest.

## Possible Extensions (good for the project report / viva)
- Replace keyword skill-matching with spaCy NER or a fine-tuned NLP model
- Add a database (SQLite/PostgreSQL) to store job postings and applicant history
- Add authentication so recruiters and candidates have separate logins
- Use sentence embeddings (e.g. `sentence-transformers`) instead of TF-IDF
  for deeper semantic matching
- Add a "explain this score" panel showing exactly which sentences
  contributed to the similarity score
- Deploy on Render/Railway/Heroku with a public link for your demo

## Notes
- Max upload size is capped at 10 MB total (configurable in `app.py`).
- `app.secret_key` is a placeholder — change it before any real deployment.
- Tested with PDF and DOCX resumes; TXT is also supported.
