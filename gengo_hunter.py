print("CIAO GITHUB")

import os

print("Token presente:", bool(os.environ.get("TELEGRAM_TOKEN")))
print("Chat presente:", bool(os.environ.get("CHAT_ID")))
if __name__ == "__main__":
    main()
