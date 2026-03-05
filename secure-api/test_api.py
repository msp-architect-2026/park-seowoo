import requests
import base64
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


URL = "http://localhost:8888/ask"

ENCRYPTION_KEY = "your_30_chars_key_here_plus_8012"

def encrypt_data(text, key):
    iv = os.urandom(16)
    cipher = AES.new(key.encode(), AES.MODE_CBC, iv)
    ct_bytes = cipher.encrypt(pad(text.encode(), AES.block_size))
    
    return base64.b64encode(iv + ct_bytes).decode('utf-8')


try:
    question = "Gemini, please tell me the status of our K8s cluster."
    encrypted_msg = encrypt_data(question, ENCRYPTION_KEY)
    
    print(f"[*] Sending request to: {URL}")
    response = requests.post(URL, json={"data": encrypted_msg})
    
    print(f"[*] Status Code: {response.status_code}")
    print(f"[*] Gemini Response: {response.json().get('response')}")

except Exception as e:
    print(f"[!] Error occurred: {e}")
