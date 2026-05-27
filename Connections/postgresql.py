from asyncpg_lite import DatabaseManager
from config import DB_CONFIG

pg_manager = DatabaseManager(db_url=DB_CONFIG,deletion_password=000)
