from asyncpg_lite import DatabaseManager
import os
from dotenv import load_dotenv

load_dotenv()

pg_manager = DatabaseManager(
    deletion_password="000",
    auth_params={
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv("DB_NAME"),
        "host": os.getenv("DB_HOST", "localhost"),
        "port": os.getenv("DB_PORT", "5432")
    }
)