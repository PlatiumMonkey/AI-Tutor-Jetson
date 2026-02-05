# File: src/core/llm_engine.py
import requests
import json

class LLMEngine:
    def __init__(self):
        # Địa chỉ của Ollama trong mạng nội bộ Docker (xem docker-compose.yaml)
        self.ollama_url = "http://ollama:11434/api/generate"
        
        # Tên model đã tải (đảm bảo khớp với cái bạn đã pull)
        self.model_name = "llama3.2:3b"
        
        # CẤU HÌNH TỐI ƯU CHO JETSON (Giai đoạn 3.1)
        # temperature: 0.7 (Sáng tạo vừa đủ, không bịa đặt)
        # top_k: 40 (Lọc bớt các từ xác suất thấp giúp chạy nhanh hơn)
        # num_ctx: 2048 (Độ dài ngữ cảnh, giảm xuống nếu tràn RAM)
        self.config = {
            "temperature": 0.7,
            "top_k": 40,
            "top_p": 0.9,
            "num_ctx": 2048, 
            "num_predict": 512, # Giới hạn số từ trả lời để không chờ lâu
            "repeat_penalty": 1.1 # Tránh lặp từ
        }

    def generate_response(self, prompt: str, system_prompt: str = None):
        """
        Gửi yêu cầu sang Ollama và nhận phản hồi streaming hoặc full text
        """
        try:
            # Chuẩn bị payload
            final_prompt = prompt
            if system_prompt:
                # Ghép vai trò (System Prompt) vào đầu
                final_prompt = f"<|system|>\n{system_prompt}\n<|user|>\n{prompt}\n<|assistant|>"

            payload = {
                "model": self.model_name,
                "prompt": final_prompt,
                "stream": False, # Tạm thời tắt stream để dễ debug
                "options": self.config
            }

            print(f"🤖 Đang gửi yêu cầu tới {self.model_name}...")
            
            # Gọi API
            response = requests.post(self.ollama_url, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "")
            else:
                return f"Lỗi Ollama: {response.status_code} - {response.text}"

        except Exception as e:
            return f"Lỗi kết nối LLM Engine: {str(e)}"

# Test chạy độc lập
if __name__ == "__main__":
    llm = LLMEngine()
    print(llm.generate_response("Hello, are you ready?"))