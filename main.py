import os
from dotenv import load_dotenv
load_dotenv()

print(os.getenv("OPEN_API_KEY"))
print(os.getenv("DISCORD_TOKEN"))
print(os.getenv("DATABASE_URL"))
