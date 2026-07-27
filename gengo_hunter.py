import os
import json
import hashlib
import requests
import feedparser


RSS_URL = "https://gengo.com/rss/available_jobs/7f2172912f19d67534e9668a57900dec5545d95a20652351863981/"


TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]


MEMORY_FILE = "seen_jobs.json"


print("🚀 Gengo Hunter avviato")


def send_telegram(message):

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message,
        "disable_web_page_preview": False
    }

    response = requests.post(
        url,
        json=data,
        timeout=10
    )

    print("Telegram status:", response.status_code)
    print(response.text)



def load_seen():

    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)

    except:
        return []



def save_seen(data):

    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f)



def get_feed():

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; Feeder RSS Reader)"
    }

    try:

        response = requests.get(
            RSS_URL,
            headers=headers,
            timeout=15
        )

        print("HTTP Gengo:", response.status_code)

        if response.status_code != 200:
            print("Feed non disponibile")
            return None


        return feedparser.parse(response.text)


    except Exception as e:

        print("Errore lettura feed:", e)
        return None



def main():

    seen = load_seen()

    feed = get_feed()


    if feed is None:
        return


    print("Jobs trovati:", len(feed.entries))


    for entry in feed.entries:


        job_id = hashlib.md5(
            entry.link.encode()
        ).hexdigest()


        if job_id in seen:
            continue


        message = f"""
🚨 GENGO JOB DISPONIBILE

🌍 EN → IT

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

if __name__ == "__main__":
    main()
