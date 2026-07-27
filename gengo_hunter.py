import os
import json
import hashlib
import requests
import feedparser


RSS_URL = "https://gengo.com/rss/available_jobs/7f2172912f19d67534e9668a57900dec5545d95a20652351863981/"


TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]


MEMORY_FILE = "seen_jobs.json"



def send_telegram(message):

    url = (
        f"https://api.telegram.org/bot"
        f"{TELEGRAM_TOKEN}/sendMessage"
    )

    data = {
        "chat_id": CHAT_ID,
        "text": message,
        "disable_web_page_preview": False
    }

    requests.post(url, json=data)



def load_seen():

    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)

    except:
        return []



def save_seen(data):

    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f)



def main():

    seen = load_seen()

    feed = feedparser.parse(RSS_URL)


    for entry in feed.entries:


        job_id = hashlib.md5(
            entry.link.encode()
        ).hexdigest()


        if job_id in seen:
            continue


        message = f"""
🚨 GENGO JOB DISPONIBILE

🌐 EN → IT

📌 {entry.title}

📝 {entry.description}

🔗 Apri lavoro:
{entry.link}
"""


        send_telegram(message)


        seen.append(job_id)



    save_seen(seen)



if __name__ == "__main__":
    main()
