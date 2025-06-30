import schedule
import time
from main import fetch_headlines, cluster_headlines, summarize_cluster, TOPICS
from email_utils import send_email
import os
from dotenv import load_dotenv

load_dotenv()
EMAIL = os.getenv("GMAIL_USER")
PASS = os.getenv("GMAIL_APP_PASSWORD")

def run_daily_summary():
    headlines = []
    for topic in TOPICS:
        headlines += fetch_headlines(topic)
    clusters = cluster_headlines(headlines, n_clusters=5)
    summary = ""
    for i, (cluster_id, titles) in enumerate(clusters.items(), start=1):
        summary += f"Topic {i}\n"
        summary += summarize_cluster(titles) + "\n\n"
    send_email(
        subject="Inner Loop Daily Trend Brief",
        body=summary,
        to_email=EMAIL,
        from_email=EMAIL,
        app_password=PASS
    )

schedule.every().day.at("08:00").do(run_daily_summary)

while True:
    schedule.run_pending()
    time.sleep(60)
