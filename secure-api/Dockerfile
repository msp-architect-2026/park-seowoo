FROM python:3.10-slim

WORKDIR /app

# 1. MariaDB 및 컴파일용 리눅스 패키지 설치 (필수)
RUN apt-get update && apt-get install -y \
    gcc \
    libmariadb-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. 파이썬 라이브러리 통함 설치 (오타 및 누락 방지 완결판)
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    groq \
    openai \
    python-multipart \
    cryptography \
    mariadb \
    python-jose[cryptography] \
    passlib[bcrypt] \
    pycryptodome \
    mysql-connector-python

# 3. 소스 코드 복사
COPY . .

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# 4. 실행 설정
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
