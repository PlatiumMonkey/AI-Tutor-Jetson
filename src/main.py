# File: src/main.py
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import uvicorn
import sys
import os
from src.core.llm_engine import LLMEngine

# 1. Khởi tạo App
app = FastAPI(
    title="AI Tutor Jetson API",
    description="Backend API cho Chatbot học tập chạy trên Jetson Orin Nano",
    version="1.0.0"
)

# --- KHỞI TẠO GLOBAL VAR ---
llm_bot = None

@app.on_event("startup")
async def startup_event():
    """Hàm này sẽ chạy 1 lần duy nhất khi Server bật"""
    global llm_bot
    print("Đang khởi động LLM Engine...")
    try:
        llm_bot = LLMEngine()
        print("Kết nối LLM thành công! Sẵn sàng phục vụ.")
    except Exception as e:
        print(f"Lỗi khởi tạo LLM: {e}")
        llm_bot = None

# 2. Định nghĩa cấu trúc dữ liệu đầu vào
class ChatRequest(BaseModel):
    user_message: str
    session_id: str = "default_session"

# 3. Tạo API kiểm tra sức khỏe (Health Check)
@app.get("/")
async def root():
    status = "ready" if llm_bot else "initializing_or_error"
    return {
        "status": status, 
        "device": "Jetson Orin Nano", 
        "model": "llama3.2:3b"
    }

# 4. Tạo API Chat cơ bản (sẽ kết nối Ollama sau)
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    global llm_bot
    
    # Kiểm tra biến toàn cục
    if llm_bot is None:
        return {
            "reply": "⚠️ Hệ thống đang khởi động hoặc gặp lỗi kết nối Ollama. Vui lòng thử lại sau 30 giây."
        }
        
    user_msg = request.user_message
    
    # System Prompt cho vai trò Gia sư
    system_role = (
        "Bạn là AI Tutor (Trợ lý ảo dạy tiếng Anh). "
        "Nhiệm vụ: Trả lời ngắn gọn, sửa lỗi ngữ pháp cho người dùng nếu có. "
        "Luôn khích lệ người học."
    )
    
    # Gọi Model
    try:
        ai_reply = llm_bot.generate_response(
            prompt=user_msg, 
            system_prompt=system_role
        )
    except Exception as e:
        ai_reply = f"Lỗi xử lý: {str(e)}"
    
    return {"reply": ai_reply}

# 5. Chạy Server (nếu chạy trực tiếp file này)
if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)