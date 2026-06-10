from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

TOKEN = os.getenv("TOKEN")
DB_CONFIG = os.getenv("DB_URL")