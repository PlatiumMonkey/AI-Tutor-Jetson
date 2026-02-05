import streamlit as st
import requests

# Cấu hình trang
st.set_page_config(page_title="AI English Tutor", layout="wide")

# Địa chỉ API Backend (file main.py)
# Lưu ý: Khi chạy trong Docker, localhost của container này không gọi được container kia
# Chúng ta sẽ dùng tên service trong docker-compose (sẽ cấu hình ở bước 3)
API_URL = "http://app-backend:8000" 

# --- THANH BÊN (SIDEBAR) ---
st.sidebar.title("🎓 AI Tutor Menu")
option = st.sidebar.radio(
    "Chọn chức năng:",
    ["🤖 Chat Tự Do", "📝 Sửa Lỗi Ngữ Pháp", "🗣️ Luyện Phát Âm"]
)

st.sidebar.markdown("---")
st.sidebar.info("Hệ thống chạy trên Jetson Orin Nano")

# --- CHỨC NĂNG 1: CHAT TỰ DO ---
if option == "🤖 Chat Tự Do":
    st.header("Trò chuyện & Học tập")
    
    # Khởi tạo lịch sử chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Hiển thị lịch sử
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Nhập câu hỏi
    if prompt := st.chat_input("Nhập tin nhắn tiếng Anh..."):
        # 1. Hiển thị câu hỏi của user
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 2. Gọi API Backend (main.py)
        try:
            # Gửi request sang Backend
            payload = {"user_message": prompt, "session_id": "streamlit_user"}
            response = requests.post(f"{API_URL}/chat", json=payload)
            
            if response.status_code == 200:
                bot_reply = response.json().get("reply", "Lỗi phản hồi.")
            else:
                bot_reply = "Không kết nối được với Backend AI."
        except Exception as e:
            bot_reply = f"Lỗi kết nối: {str(e)}"

        # 3. Hiển thị câu trả lời của Bot
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        with st.chat_message("assistant"):
            st.markdown(bot_reply)

# --- CHỨC NĂNG 2: SỬA LỖI NGỮ PHÁP ---
elif option == "📝 Sửa Lỗi Ngữ Pháp":
    st.header("Công cụ Chấm chữa Ngữ pháp")
    text_input = st.text_area("Dán đoạn văn tiếng Anh của bạn vào đây:", height=150)
    
    if st.button("Kiểm tra ngay"):
        if text_input:
            st.success("Đang phân tích... (Tính năng này sẽ gọi API phân tích ngữ pháp)")
            # Sau này sẽ gọi API /grammar-check ở đây
            st.info(f"Đoạn văn gốc: {text_input}")
            st.warning("Gợi ý sửa: (AI sẽ trả về kết quả tại đây)")
        else:
            st.error("Vui lòng nhập văn bản.")

# --- CHỨC NĂNG 3: LUYỆN PHÁT ÂM ---
elif option == "🗣️ Luyện Phát Âm":
    st.header("Luyện Nói (Speaking Practice)")
    st.write("Nhấn nút bên dưới để ghi âm và AI sẽ chấm điểm.")
    
    # Placeholder cho nút ghi âm (sẽ cài thư viện sau)
    st.button("🎙️ Bắt đầu ghi âm")
    st.caption("Tính năng đang phát triển...")