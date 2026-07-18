"""
send_email.py
Sends today's top job matches to your inbox using Gmail's free SMTP.

Setup (one-time, free):
  1. Turn on 2-Step Verification on your Google account.
  2. Create an "App Password": https://myaccount.google.com/apppasswords
  3. In your GitHub repo -> Settings -> Secrets and variables -> Actions,
     add these repo secrets:
       EMAIL_ADDRESS   = your_gmail@gmail.com
       EMAIL_APP_PASS  = the 16-character app password
       EMAIL_TO        = where you want results sent (can be same address)

No paid service required — Gmail SMTP is free for personal-volume sending.
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def build_email_body(jobs, profile_name):
    if not jobs:
        return f"<p>Hi {profile_name}, no strong matches found today. More tomorrow!</p>"

    rows = ""
    for j in jobs:
        rows += f"""
        <div style="margin-bottom:16px;padding:14px;border:1px solid #ddd;border-radius:8px;">
          <a href="{j.get('url','#')}" style="font-weight:bold;font-size:15px;text-decoration:none;">
            {j.get('title','Untitled')}
          </a>
          <div style="color:#666;font-size:13px;">
            {j.get('company','Unknown')} &middot; {j.get('location','N/A')} &middot; via {j.get('source','')}
          </div>
          <div style="color:#2a9d8f;font-size:12px;margin-top:6px;">
            match score: {j.get('match_score',0)} | skills: {", ".join(j.get('matched_skills', []))}
          </div>
        </div>
        """

    return f"""
    <html><body style="font-family:sans-serif;">
      <h2>Hi {profile_name}, here are today's top {len(jobs)} matches</h2>
      {rows}
      <p style="color:#999;font-size:12px;">Sent automatically by your self-built Job Agent 🤖</p>
    </body></html>
    """


def send(jobs, config):
    profile = config["profile"]

    sender = os.environ.get("EMAIL_ADDRESS")
    app_password = os.environ.get("EMAIL_APP_PASS")
    recipient = os.environ.get("EMAIL_TO", sender)

    if not sender or not app_password:
        print("[send_email] EMAIL_ADDRESS / EMAIL_APP_PASS not set — skipping email send.")
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🎯 {len(jobs)} job matches for you — {profile.get('role_target','')}"
    msg["From"] = sender
    msg["To"] = recipient
    msg.attach(MIMEText(build_email_body(jobs, profile.get("name", "there")), "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, app_password)
            server.sendmail(sender, recipient, msg.as_string())
        print(f"[send_email] sent to {recipient}")
    except Exception as e:
        print(f"[send_email] failed: {e}")
