"""
match_jobs.py
Scores each fetched job against the user's skills/config using a
transparent, explainable keyword-matching algorithm (no paid LLM needed).

Scoring logic:
  +2 points  for each core skill found in title+description
  +1 point   for each nice-to-have keyword found
  -3 points  for each exclude keyword found (e.g. "Senior", "10+ years")
  +1 point   if location matches a preferred location or is remote

This is intentionally simple and readable — a good thing to explain
in an interview: "I built a weighted keyword scorer, here's the logic..."
You can later swap this for TF-IDF/embeddings as a v2 upgrade.
"""

import re


def _text_blob(job):
    return f"{job.get('title','')} {job.get('description','')} {' '.join(job.get('tags', []))}".lower()


def score_job(job, config):
    profile = config["profile"]
    text = _text_blob(job)
    score = 0
    matched_skills = []

    for skill in profile.get("skills", []):
        if re.search(rf"\b{re.escape(skill.lower())}\b", text):
            score += 2
            matched_skills.append(skill)

    for kw in profile.get("nice_to_have_keywords", []):
        if re.search(rf"\b{re.escape(kw.lower())}\b", text):
            score += 1
            matched_skills.append(kw)

    for bad in profile.get("exclude_keywords", []):
        if re.search(rf"\b{re.escape(bad.lower())}\b", text):
            score -= 3

    location = (job.get("location") or "").lower()
    preferred_locations = [l.lower() for l in profile.get("locations", [])]
    if profile.get("remote_ok") and "remote" in location:
        score += 1
    elif any(loc in location for loc in preferred_locations):
        score += 1

    return score, matched_skills


def match_all(jobs, config):
    threshold = config["matching"]["min_score_threshold"]
    max_results = config["matching"]["max_results_per_run"]

    scored = []
    for job in jobs:
        score, matched = score_job(job, config)
        if score >= threshold:
            job_copy = dict(job)
            job_copy["match_score"] = score
            job_copy["matched_skills"] = matched
            scored.append(job_copy)

    # sort best matches first
    scored.sort(key=lambda j: j["match_score"], reverse=True)
    return scored[:max_results]


if __name__ == "__main__":
    import yaml
    from fetch_jobs import fetch_all

    with open("config.yaml") as f:
        cfg = yaml.safe_load(f)

    jobs = fetch_all()
    top = match_all(jobs, cfg)
    for j in top:
        print(f"[{j['match_score']}] {j['title']} @ {j['company']} ({j['source']})")
