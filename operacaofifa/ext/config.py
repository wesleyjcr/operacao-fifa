import os
from dotenv import load_dotenv

load_dotenv('.env')

bot_token = os.getenv("BOT_TOKEN")
bot_user_name = os.getenv("BOT_USERNAME")
URL = os.getenv("URL")
