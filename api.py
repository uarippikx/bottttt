from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from Connections.postgresql import pg_manager as manager

# Создание приложения FastAPI
app = FastAPI(title="Profile API", version="1.0.0")

# CORS middleware - разрешить запросы с GitHub Pages и других источников
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://uarippikx.github.io",
     "http://localhost:3000",  # Для локальной разработки
    "http://localhost:8000"] # Явно указываем ваш фронтенд
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], # Позволит фронтенду передавать заголовок ngrok-skip-browser-warning
)

# ===== Health Check =====
@app.get("/health")
async def health_check():
    """Проверка доступности API"""
    return {"status": "ok", "message": "API is running"}

# ===== Profile Endpoint =====
@app.get("/api/profile")
async def get_profile(user_id: int):
    """
    Получить профиль пользователя
    
    Args:
        user_id (int): ID пользователя из Telegram
    
    Returns:
        {
            "user_id": int,
            "username": str,
            "email": str
        }
    """
    try:
        if not user_id or user_id <= 0:
            raise HTTPException(status_code=400, detail="Invalid user_id")
        
        # Запрос данных из БД
        async with manager:
            user = await manager.select_data(
                table_name="userssdata",
                where_dict={"user_id": user_id},
                one_dict=True
            )
        
        # Проверка результата
        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found in database"
            )
        
        # Возврат профиля в нужном формате
        return {
            "user_id": user_id,
            "username": user.get('username', 'Unknown'),
            "email": user.get('email', '')
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching profile: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

# ===== Run Server =====
if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )