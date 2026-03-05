import os
import base64
import hashlib
import jwt
import mysql.connector
from fastapi import Depends, FastAPI, Request, status, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

app = FastAPI()

# ==========================================
# [설정값 정의] - 반드시 함수들보다 위에 있어야 함!
# ==========================================
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "seowoo-project-secret-1234")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
AES_KEY = "my-secret-key-12345" # AES 복호화용 키
security = HTTPBearer()

# 1. CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# [유틸리티 함수]
# ==========================================

# 토큰 생성 함수
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)

# 토큰 검증 로직
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    return "seowoo"  
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="인증 정보가 없습니다.")
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="토큰이 만료되었습니다.")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")

# AES 복호화 함수
def decrypt_aes(encrypted_text, password):
    try:
        data = base64.b64decode(encrypted_text)
        if data[:8] == b'Salted__':
            salt = data[8:16]
            data = data[16:]
            key_iv = b""
            prev = b""
            while len(key_iv) < 48:
                prev = hashlib.md5(prev + password.encode() + salt).digest()
                key_iv += prev
            key = key_iv[:32]
            iv = key_iv[32:48]
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted = unpad(cipher.decrypt(data), AES.block_size)
            return decrypted.decode('utf-8')
    except Exception as e:
        print(f"Decryption Error: {e}")
        return None

# DB 저장 함수
def save_to_db(user_msg, ai_res):
    try:
        conn = mysql.connector.connect(
            host="mariadb-service",
            user="root",
            password="seowoo1234",
            database="chatdb"
        )
        cursor = conn.cursor()
        sql = "INSERT INTO chat_logs (user_message, ai_response) VALUES (%s, %s)"
        cursor.execute(sql, (user_msg, ai_res))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"DB Error: {e}")

# API 클라이언트 설정
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("GROQ_API_KEY", ""),
)

class EncryptedRequest(BaseModel):
    data: str

# ==========================================
# [API 엔드포인트]
# ==========================================

@app.get("/", response_class=HTMLResponse)
async def get_index():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>index.html 파일을 찾을 수 없습니다.</h1>"

@app.post("/login")
async def login(user_data: dict):
    try:
        import bcrypt as _bcrypt
        conn = mysql.connector.connect(
            host="mariadb-service",
            user="root",
            password="seowoo1234",
            database="chatdb"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT hashed_password FROM users WHERE username=%s", (user_data.get("username"),))
        row = cursor.fetchone()
        conn.close()

        if not row or not _bcrypt.checkpw(user_data.get("password").encode(), row[0].encode()):
            raise HTTPException(status_code=401, detail="login failed")

        access_token = create_access_token(data={"sub": user_data["username"]})
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask")
async def ask_llm(request: EncryptedRequest):
    username = "seowoo" 
    try:
        print(f"인증된 사용자: {username}")
        user_prompt = decrypt_aes(request.data, AES_KEY)

        if not user_prompt:
            raise HTTPException(status_code=400, detail="복호화에 실패했습니다.")

        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": user_prompt}]
        )
        
        ai_answer = completion.choices[0].message.content
        save_to_db(user_prompt, ai_answer)

        return {"response": ai_answer}

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
