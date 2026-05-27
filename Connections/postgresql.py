from asyncpg_lite import DatabaseManager

pg_manager = DatabaseManager(
    db_url="postgresql://postgres:1234@localhost:5432/first",
    deletion_password=228)#пароль на запросы с удалением информамции в бд
