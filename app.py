# app.py
# AI-Powered Resume Screening & Job-Matching System
# Flask backend: handles JD input, multiple resume uploads,
# runs matching, and renders a ranked results page.

import os
from io import BytesIO
# pyrefly: ignore [missing-import]
from flask import Flask, render_template, request, redirect, url_for, flash

from utils import extract_text, compute_match, extract_skills

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, "uploads")
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB total upload cap

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-if-deploying"  # fine for a college project
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/match", methods=["POST"])
def match():
    jd_text_input = request.form.get("job_description", "").strip()
    resume_files = request.files.getlist("resumes")

    # ---- basic validation ----
    if not jd_text_input:
        flash("Please paste or type a job description.")
        return redirect(url_for("index"))

    if not resume_files or resume_files[0].filename == "":
        flash("Please upload at least one resume (PDF, DOCX, or TXT).")
        return redirect(url_for("index"))

    results = []
    skipped = []

    for file in resume_files:
        if file and file.filename and allowed_file(file.filename):
            try:
                file_bytes = file.read()
                text = extract_text(BytesIO(file_bytes), file.filename)
                if not text.strip():
                    skipped.append((file.filename, "No extractable text found"))
                    continue
                match_result = compute_match(jd_text_input, text)
                match_result["filename"] = file.filename
                results.append(match_result)
            except Exception as exc:  # keep the demo resilient to a bad file
                skipped.append((file.filename, str(exc)))
        elif file and file.filename:
            skipped.append((file.filename, "Unsupported file type"))

    # Rank candidates: highest match score first
    results.sort(key=lambda r: r["final_score"], reverse=True)
    for rank, r in enumerate(results, start=1):
        r["rank"] = rank

    jd_skill_count = len(extract_skills(jd_text_input))
    average_score = round(sum(r["final_score"] for r in results) / len(results), 2) if results else 0
    strong_matches = sum(1 for r in results if r["final_score"] >= 70)
    top_candidate = results[0]["filename"] if results else "N/A"

    return render_template(
        "results.html",
        jd_text=jd_text_input,
        results=results,
        skipped=skipped,
        jd_skill_count=jd_skill_count,
        average_score=average_score,
        strong_matches=strong_matches,
        top_candidate=top_candidate,
    )


if __name__ == "__main__":
    # host=0.0.0.0 so it's reachable if you run this on a lab machine/VM too
    app.run(debug=True, host="0.0.0.0", port=5000)
