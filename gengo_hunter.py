print("CIAO GITHUB ACTIONS")

import os

print("Token presente:", bool(os.environ.get("TELEGRAM_TOKEN")))
print("Chat presente:", bool(os.environ.get("CHAT_ID")))

print("FINE TEST")
