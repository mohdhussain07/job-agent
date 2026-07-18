"""
fetch_jobs.py
Pulls raw job listings from FREE, no-signup-required job APIs.

Sources used:
  1. RemoteOK      -> https://remoteok.com/api                (free, no key)
  2. Arbeitnow     -> https://www.arbeitnow.com/api/job-board-api (free, no key)

Both return JSON. We normalize them into one common shape:
  { title, company, location, description, url, source, posted_at }

Add more sources later (Adzuna, Jooble) by getting a free API key and
adding a fetch_<source>() function below — just keep the same return shape.
"""

import requests
from datetime import datetime, timezone

HEADERS = {"User-Agent": "job-agent-portfolio-project/1.0"}


def fetch_remoteok():
    """RemoteOK public API — first item is metadata, skip it."""
    jobs = []
    try:
        resp = requests.get("https://remoteok.com/api", headers=HEADERS, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        for item in data[1:]:  # skip metadata row
            jobs.append({
                "title": item.get("position", "").strip(),
                "company": item.get("company", "").strip(),
                "location": item.get("location", "Remote") or "Remote",
                "description": (item.get("description") or "")[:2000],
                "url": item.get("url", ""),
                "source": "RemoteOK",
                "posted_at": item.get("date", ""),
                "tags": item.get("tags", []),
            })
    except Exception as e:
        print(f"[fetch_remoteok] failed: {e}")
    return jobs


def fetch_arbeitnow():
    """Arbeitnow public job board API."""
    jobs = []
    try:
        resp = requests.get(
            "https://www.arbeitnow.com/api/job-board-api", headers=HEADERS, timeout=15
        )
        resp.raise_for_status()
        data = resp.json()
        for item in data.get("data", []):
            jobs.append({
                "title": item.get("title", "").strip(),
                "company": item.get("company_name", "").strip(),
                "location": item.get("location", "Remote") or "Remote",
                "description": (item.get("description") or "")[:2000],
                "url": item.get("url", ""),
                "source": "Arbeitnow",
                "posted_at": datetime.fromtimestamp(
                    item.get("created_at", 0), tz=timezone.utc
                ).isoformat() if item.get("created_at") else "",
                "tags": item.get("tags", []),
            })
    except Exception as e:
        print(f"[fetch_arbeitnow] failed: {e}")
    return jobs


def fetch_all():
    """Combine all sources into one list."""
    all_jobs = []
    all_jobs.extend(fetch_remoteok())
    all_jobs.extend(fetch_arbeitnow())
    print(f"[fetch_all] fetched {len(all_jobs)} total raw jobs")
    return all_jobs


if __name__ == "__main__":
    jobs = fetch_all()
    print(f"Sample job: {jobs[0] if jobs else 'none found'}")
