from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import traceback 

from Connections.postgresql import pg_manager as manager

app = FastAPI(title="Profile API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://uarippikx.github.io"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== Health Check =====
@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "API is running"}

# ===== Get Profile =====
@app.get("/api/profile")
async def get_profile(user_id: int):
    try:
        if not user_id or user_id <= 0:
            raise HTTPException(status_code=400, detail="Invalid user_id")
        
        async with manager:
            user = await manager.select_data(
                table_name="userssdata",
                where_dict={"user_id": user_id},
                one_dict=True
            )
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found in database")
        
        return {
            "user_id": user_id,
            "username": user.get('username', 'Unknown'),
            "email": user.get('email', '')
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching profile: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal server error")

# ===== Update Email =====
class UpdateEmailRequest(BaseModel):
    user_id: int
    new_email: str
    password: str

@app.post("/api/profile/update")
async def update_profile(body: UpdateEmailRequest):
    try:
        async with manager:
            user = await manager.select_data(
                table_name="userssdata",
                where_dict={"user_id": body.user_id},
                one_dict=True
            )
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if user.get("password") != body.password:
            raise HTTPException(status_code=403, detail="Неверный пароль")
        
        async with manager:
            await manager.update_data(
                table_name="userssdata",
                where_dict={"user_id": body.user_id},
                update_dict={"email": body.new_email}
            )
        
        return {"email": body.new_email}
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error updating email: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal server error")

# ===== Run Server =====
if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )