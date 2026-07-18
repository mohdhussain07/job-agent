"""
main.py
Orchestrates the full daily pipeline:
  1. fetch jobs from free APIs
  2. score/match against your skills (config.yaml)
  3. write the dashboard (docs/index.html + docs/jobs.json)
  4. email you the results

Run locally with:  python main.py
Runs automatically every day via .github/workflows/daily.yml
"""

import sys
import yaml

sys.path.insert(0, "scripts")

from fetch_jobs import fetch_all
from match_jobs import match_all
from generate_dashboard import generate as generate_dashboard
from send_email import send as send_email


def main():
    with open("config.yaml") as f:
        config = yaml.safe_load(f)

    print("Step 1/4: fetching jobs...")
    raw_jobs = fetch_all()

    print("Step 2/4: matching against your skills...")
    top_jobs = match_all(raw_jobs, config)
    print(f"  -> {len(top_jobs)} jobs passed the threshold")

    print("Step 3/4: building dashboard...")
    generate_dashboard(top_jobs, config)

    print("Step 4/4: sending email...")
    send_email(top_jobs, config)

    print("Done.")


if __name__ == "__main__":
    main()
