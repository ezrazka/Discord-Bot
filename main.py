import os
from dotenv import load_dotenv

from src import bot

load_dotenv()

token = os.environ.get("TOKEN")

if __name__ == "__main__":
    keep_alive()
    bot.run(token)
