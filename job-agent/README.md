# 🎯 Job Agent — Personal AI-Powered Job Recommender

A fully automated, **100% free** job-matching agent that:
- Pulls fresh listings daily from free public job APIs (RemoteOK, Arbeitnow)
- Scores each job against your skills using a weighted keyword-matching algorithm
- Publishes a live dashboard via GitHub Pages
- Emails you the top 5–10 matches every morning

No paid APIs, no paid hosting, no subscriptions. Runs entirely on GitHub's free tier.

## How it works

```
GitHub Actions (daily cron, free)
        │
        ▼
  fetch_jobs.py  ──►  pulls raw listings from RemoteOK + Arbeitnow APIs
        │
        ▼
  match_jobs.py  ──►  scores each job against config.yaml (your skills)
        │
        ▼
generate_dashboard.py ──► writes docs/index.html + docs/jobs.json
        │
        ▼
  send_email.py  ──►  emails you the top matches via Gmail SMTP
        │
        ▼
  git commit + push  ──►  updates your live GitHub Pages dashboard
```

## Setup (10 minutes, all free)

### 1. Edit `config.yaml`
Add your real skills, target role, and preferences. This drives the matching algorithm.

### 2. Push this repo to GitHub
```bash
git init
git add .
git commit -m "Initial commit: job agent"
git remote add origin https://github.com/<your-username>/job-agent.git
git push -u origin main
```

### 3. Enable GitHub Pages
Repo → **Settings → Pages** → Source: `main` branch, folder: `/docs` → Save.
Your dashboard will be live at `https://<your-username>.github.io/job-agent/`

### 4. (Optional but recommended) Enable email delivery
1. Turn on 2-Step Verification on your Google account.
2. Create a free [Google App Password](https://myaccount.google.com/apppasswords).
3. In your repo: **Settings → Secrets and variables → Actions → New repository secret**, add:
   - `EMAIL_ADDRESS` → your Gmail address
   - `EMAIL_APP_PASS` → the 16-character app password
   - `EMAIL_TO` → where you want results delivered

### 5. Test it
Go to the **Actions** tab → **Daily Job Agent Run** → **Run workflow** (manual trigger).
Check the logs, then check your dashboard and inbox.

It will now run automatically every day at 6:00 AM UTC — edit the cron
schedule in `.github/workflows/daily.yml` to change the time.

## Run locally (for development)
```bash
pip install -r requirements.txt
python main.py
```

## Why this is a good portfolio project
- **Real automation**: uses GitHub Actions cron, not a toy script you run manually
- **Explainable algorithm**: the scoring logic in `match_jobs.py` is transparent
  and easy to walk through in an interview — no black-box LLM call
- **Live demo**: the GitHub Pages dashboard is a shareable link for your resume
- **Extensible**: clear places to plug in more job sources (Adzuna, Jooble),
  swap the scorer for TF-IDF/embeddings, or add Slack/Telegram delivery

## Roadmap ideas (good "future work" talking points)
- [ ] Add Adzuna and Jooble as extra sources (free API keys, more geographic coverage)
- [ ] Swap keyword scoring for TF-IDF or sentence-embedding similarity
- [ ] Add a "resume paste" mode that auto-extracts skills instead of manual config
- [ ] Telegram bot delivery as an alternative to email
- [ ] Track applied/not-applied status per job in the dashboard

## License
MIT — do whatever you want with it.
