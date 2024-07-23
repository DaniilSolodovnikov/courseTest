import os


# Redis Configuration
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))


# Central Bank URL
CB_URL = "https://cbr.ru/scripts/XML_daily.asp"


# Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN")


# Logging Level
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")