import os
from dotenv import load_dotenv
from bot import run_discord_bot
import database

def main():
    database.create_tables()  # Ensure tables are created
    run_discord_bot()  # Start the bot

if __name__ == "__main__":
    main()