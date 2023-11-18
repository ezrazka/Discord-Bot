import os
from dotenv import load_dotenv

from keep_alive import keep_alive
from src import bot

load_dotenv()

token = os.environ.get("TOKEN")

if __name__ == "__main__":
    keep_alive()
    bot.run(token)
