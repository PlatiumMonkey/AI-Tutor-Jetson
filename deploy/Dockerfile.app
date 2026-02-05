FROM python:3.10-slim

WORKDIR /app

# Cài đặt các thư viện hệ thống cần thiết (nếu cần cho Audio/PDF)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy file requirements và cài đặt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/

# Mở cổng 8000
EXPOSE 8000

# Lệnh chạy mặc định (có thể bị ghi đè bởi docker-compose)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]