import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
AUTH_LOG_PATH = os.getenv("AUTH_LOG_PATH", "/var/log/auth.log")
KEYWORDS = os.getenv("KEYWORDS", "Failed password,Invalid user").split(",")
IGNORE_KEYWORDS = os.getenv("IGNORE_KEYWORDS", "").split(",")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 2))

def send_alert(message):
    try:
        payload = {"content": f"🚨 SSH 접근 시도 감지됨\n```{message}```"}
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        if response.status_code != 204:
            print(f"[!] 디스코드 전송 실패: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[!] 웹훅 전송 중 오류: {e}")

def tail_file(path):
    with open(path, 'r') as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if not line:
                time.sleep(CHECK_INTERVAL)
                continue
            if any(keyword in line for keyword in KEYWORDS) and not any(ignore in line for ignore in IGNORE_KEYWORDS):
                print(f"[!] 접근 시도 탐지: {line.strip()}")
                send_alert(line.strip())
                with open("intrusion.log", "a") as logf:
                    logf.write(line)

if __name__ == "__main__":
    print("[*] SSH 접근 감시 시작")
    tail_file(AUTH_LOG_PATH)