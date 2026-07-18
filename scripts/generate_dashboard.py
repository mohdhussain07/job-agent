"""
generate_dashboard.py
Writes docs/jobs.json (raw data) and docs/index.html (a clean static
dashboard) so GitHub Pages can serve it for free at:
  https://<your-username>.github.io/job-agent/
"""

import json
from datetime import datetime, timezone

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name}'s Job Agent — Daily Matches</title>
<style>
  :root {{
    --bg: #0f1115; --card: #171a21; --text: #e8e8ec; --muted: #9a9ea8;
    --accent: #6ee7b7; --border: #262a33;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    background: var(--bg); color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    margin: 0; padding: 40px 20px;
  }}
  .wrap {{ max-width: 760px; margin: 0 auto; }}
  h1 {{ font-size: 1.6rem; margin-bottom: 4px; }}
  .sub {{ color: var(--muted); margin-bottom: 28px; font-size: 0.9rem; }}
  .job {{
    background: var(--card); border: 1px solid var(--border);
    border-radius: 12px; padding: 18px 20px; margin-bottom: 14px;
  }}
  .job-top {{ display: flex; justify-content: space-between; align-items: baseline; gap: 12px; }}
  .job-title {{ font-weight: 600; font-size: 1.05rem; }}
  .job-score {{
    background: rgba(110,231,183,0.12); color: var(--accent);
    padding: 2px 10px; border-radius: 999px; font-size: 0.8rem; white-space: nowrap;
  }}
  .job-meta {{ color: var(--muted); font-size: 0.85rem; margin-top: 4px; }}
  .job-skills {{ margin-top: 10px; font-size: 0.8rem; color: var(--accent); }}
  a {{ color: var(--accent); text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  .empty {{ color: var(--muted); text-align: center; padding: 40px 0; }}
</style>
</head>
<body>
<div class="wrap">
  <h1>{name}'s Job Agent</h1>
  <div class="sub">Last updated: {updated} &middot; {count} matches today</div>
  {jobs_html}
</div>
</body>
</html>
"""

JOB_CARD = """
  <div class="job">
    <div class="job-top">
      <div class="job-title"><a href="{url}" target="_blank">{title}</a></div>
      <div class="job-score">score {score}</div>
    </div>
    <div class="job-meta">{company} &middot; {location} &middot; via {source}</div>
    <div class="job-skills">matched: {skills}</div>
  </div>
"""


def generate(jobs, config):
    profile = config["profile"]
    out_json = config["output"]["jobs_json"]
    out_html = config["output"]["dashboard_html"]

    with open(out_json, "w") as f:
        json.dump(jobs, f, indent=2)

    if jobs:
        cards = "\n".join(
            JOB_CARD.format(
                url=j.get("url", "#"),
                title=j.get("title", "Untitled"),
                score=j.get("match_score", 0),
                company=j.get("company", "Unknown"),
                location=j.get("location", "N/A"),
                source=j.get("source", "N/A"),
                skills=", ".join(j.get("matched_skills", [])) or "—",
            )
            for j in jobs
        )
    else:
        cards = '<div class="empty">No matches today — check back tomorrow.</div>'

    html = HTML_TEMPLATE.format(
        name=profile.get("name", "Your"),
        updated=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        count=len(jobs),
        jobs_html=cards,
    )
    with open(out_html, "w") as f:
        f.write(html)

    print(f"[generate_dashboard] wrote {out_html} and {out_json} ({len(jobs)} jobs)")
