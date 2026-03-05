from flask import Flask, request, jsonify
import jwt
import datetime
import mysql.connector
import hashlib
import os

app = Flask(__name__)
JWT_SECRET = os.environ.get("JWT_SECRET_KEY", "seowoo-project-secret-key-123456")
DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "mariadb"),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", "seowoo1234"),
    "database": os.environ.get("DB_NAME", "chatdb"),
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

@app.route("/login", methods=["GET", "POST"])
def login():
    # GET 요청이면 로그인 페이지 반환
    if request.method == "GET":
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>로그인</title>
            <style>
                body { font-family: Arial; display: flex; justify-content: center;
                       align-items: center; height: 100vh; margin: 0; background: #f0f2f5; }
                .box { background: white; padding: 40px; border-radius: 10px;
                       box-shadow: 0 2px 10px rgba(0,0,0,0.1); width: 320px; }
                h2 { text-align: center; color: #333; margin-bottom: 24px; }
                input { width: 100%; padding: 10px; margin: 8px 0;
                        border: 1px solid #ddd; border-radius: 5px;
                        box-sizing: border-box; font-size: 14px; }
                button { width: 100%; padding: 12px; background: #4CAF50;
                         color: white; border: none; border-radius: 5px;
                         font-size: 16px; cursor: pointer; margin-top: 10px; }
                button:hover { background: #45a049; }
                .error { color: red; text-align: center; font-size: 13px; }
            </style>
        </head>
        <body>
            <div class="box">
                <h2>🔐 AI 서비스 로그인</h2>
                <form method="POST">
                    <input type="text" name="username" placeholder="아이디" required />
                    <input type="password" name="password" placeholder="비밀번호" required />
                    <button type="submit">로그인</button>
                </form>
            </div>
        </body>
        </html>
        ''', 200

    # POST 요청이면 인증 처리
    data = request.form if request.form else request.get_json(silent=True) or {}
    username = data.get("username", "")
    password = data.get("password", "")
    pw_hash  = hashlib.sha256(password.encode()).hexdigest()

    try:
        conn   = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, username, role FROM users WHERE username=%s AND password=%s",
            (username, pw_hash)
        )
        user = cursor.fetchone()
        cursor.close()
        conn.close()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    if not user:
        return '''
        <!DOCTYPE html><html><head><title>로그인</title>
        <style>
            body { font-family: Arial; display: flex; justify-content: center;
                   align-items: center; height: 100vh; margin: 0; background: #f0f2f5; }
            .box { background: white; padding: 40px; border-radius: 10px;
                   box-shadow: 0 2px 10px rgba(0,0,0,0.1); width: 320px; }
            h2 { text-align: center; color: #333; }
            input { width: 100%; padding: 10px; margin: 8px 0;
                    border: 1px solid #ddd; border-radius: 5px;
                    box-sizing: border-box; font-size: 14px; }
            button { width: 100%; padding: 12px; background: #4CAF50;
                     color: white; border: none; border-radius: 5px;
                     font-size: 16px; cursor: pointer; margin-top: 10px; }
            .error { color: red; text-align: center; font-size: 13px; margin-top: 10px; }
        </style></head>
        <body><div class="box">
            <h2>🔐 AI 서비스 로그인</h2>
            <form method="POST">
                <input type="text" name="username" placeholder="아이디" required />
                <input type="password" name="password" placeholder="비밀번호" required />
                <button type="submit">로그인</button>
            </form>
            <p class="error">❌ 아이디 또는 비밀번호가 틀렸습니다.</p>
        </div></body></html>
        ''', 401

    token = jwt.encode({
        "sub":      str(user["id"]),
        "username": user["username"],
        "role":     user["role"],
        "exp":      datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    }, JWT_SECRET, algorithm="HS256")

    resp = app.make_response("")
    resp.headers["Location"] = "/"
    resp.status_code = 302
    resp.set_cookie("auth_token", token, httponly=True, samesite="Lax", max_age=28800)
    return resp

@app.route("/validate", methods=["GET"])
def validate():
    token = request.cookies.get("auth_token") or \
            request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        return jsonify({"error": "No token"}), 401
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return jsonify({"user": payload["username"], "role": payload["role"]}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

@app.route("/logout")
def logout():
    resp = app.make_response("")
    resp.headers["Location"] = "/login"
    resp.status_code = 302
    resp.delete_cookie("auth_token")
    return resp

@app.route("/healthz")
def health():
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
