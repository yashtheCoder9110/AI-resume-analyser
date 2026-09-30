# utils.py
# Core logic: extracting text from uploaded files, extracting skills,
# and computing a match score between a resume and a job description.

import re
import pdfplumber
import docx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from skills_data import SKILLS_DB


# ---------------------------------------------------------------------
# 1. Text extraction
# ---------------------------------------------------------------------
def extract_text_from_pdf(file_stream) -> str:
    """Extract raw text from a PDF file object (in-memory or on disk)."""
    text_parts = []
    with pdfplumber.open(file_stream) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    return "\n".join(text_parts)


def extract_text_from_docx(file_stream) -> str:
    """Extract raw text from a .docx file object (in-memory or on disk)."""
    document = docx.Document(file_stream)
    return "\n".join(p.text for p in document.paragraphs)


def extract_text(file_stream, filename: str) -> str:
    """Dispatch to the right extractor based on file extension."""
    lower = filename.lower()
    if lower.endswith(".pdf"):
        return extract_text_from_pdf(file_stream)
    elif lower.endswith(".docx"):
        return extract_text_from_docx(file_stream)
    elif lower.endswith(".txt"):
        return file_stream.read().decode("utf-8", errors="ignore")
    else:
        raise ValueError(f"Unsupported file type: {filename}")


# ---------------------------------------------------------------------
# 2. Skill extraction
# ---------------------------------------------------------------------
def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def extract_skills(text: str) -> set:
    """
    Return the subset of SKILLS_DB that appears in `text`.
    Uses word-boundary matching so short skills like 'r' or 'c'
    don't falsely match inside other words.
    """
    normalized = _normalize(text)
    found = set()
    for skill in SKILLS_DB:
        pattern = r"(?<![a-zA-Z0-9])" + re.escape(skill) + r"(?![a-zA-Z0-9])"
        if re.search(pattern, normalized):
            found.add(skill)
    return found


# ---------------------------------------------------------------------
# 3. Similarity + scoring
# ---------------------------------------------------------------------
def text_similarity(jd_text: str, resume_text: str) -> float:
    """
    Cosine similarity between the JD and resume using TF-IDF vectors.
    Returns a value between 0 and 1.
    """
    if not jd_text.strip() or not resume_text.strip():
        return 0.0
    vectorizer = TfidfVectorizer(stop_words="english")
    try:
        tfidf_matrix = vectorizer.fit_transform([jd_text, resume_text])
    except ValueError:
        # happens if vocabulary is empty after stop-word removal
        return 0.0
    sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return float(sim)


def skill_overlap_score(jd_skills: set, resume_skills: set) -> float:
    """
    Fraction of JD-required skills that the resume also has.
    Returns 0 if the JD has no recognized skills at all.
    """
    if not jd_skills:
        return 0.0
    matched = jd_skills & resume_skills
    return len(matched) / len(jd_skills)


def compute_match(jd_text: str, resume_text: str, skill_weight: float = 0.65,
                   text_weight: float = 0.35) -> dict:
    """
    Combine skill overlap and overall text similarity into one score.
    skill_weight + text_weight should sum to 1.0.
    """
    jd_skills = extract_skills(jd_text)
    resume_skills = extract_skills(resume_text)

    s_score = skill_overlap_score(jd_skills, resume_skills)
    t_score = text_similarity(jd_text, resume_text)

    final_score = (skill_weight * s_score) + (text_weight * t_score)

    matched_skills = sorted(jd_skills & resume_skills)
    missing_skills = sorted(jd_skills - resume_skills)
    extra_skills = sorted(resume_skills - jd_skills)

    return {
        "final_score": round(final_score * 100, 2),       # percentage
        "skill_score": round(s_score * 100, 2),
        "text_score": round(t_score * 100, 2),
        "jd_skills": sorted(jd_skills),
        "resume_skills": sorted(resume_skills),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "extra_skills": extra_skills,
    }
