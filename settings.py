from dotenv import load_dotenv
from logging.config import dictConfig
import os

load_dotenv()
DISCORD_API_KEY = os.getenv("DISCORD_API_TOKEN", "U_CANT_HACK_ME")
CHANNEL_ID = os.getenv("CHANNEL_ID", "U_CANT_HACK_ME")
JOKEAPI = os.getenv("JOKE_API_TOKEN", "U_CANT_HACK_ME")
OPENAI = os.getenv("OPENAI_API_TOKEN", "U_CANT_HACK_ME")
GEMINIAI = os.getenv("GEMINI_API_TOKEN", "U_CANT_HACK_ME")
GUILD = os.getenv("GUILDS", "U_CANT_HACK_ME")
