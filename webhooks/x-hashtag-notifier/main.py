import requests
import time
import json
import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta

# 로그 설정
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "hashtag.log")
os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("HashtagMonitor")
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# 환경 변수 로드
load_dotenv()
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")  # 트위터 API 토큰
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")  # 디스코드 웹훅 URL

# 해시태그 목록 환경 변수에서 불러오기 (구분자 : ",")
HASHTAGS = [tag.strip() for tag in os.getenv("MONITOR_HASHTAGS", "#단간장터,#단간론파장터,#단간론파_장터").split(",")]

SEEN_FILE = os.getenv("SEEN_FILE", "seen_tweets.json")  # 이미 알림을 보낸 트윗 ID 저장 파일
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "60"))  # 트윗 검색 주기(초)

HEADERS = {
    "Authorization": f"Bearer {BEARER_TOKEN}"
}

# 타임존 및 시작 시간 설정
KST = timezone(timedelta(hours=9))
start_time = datetime.now(KST)
logger.info(f"🕒 봇 시작 시간 (Asia/Seoul 기준): {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

# 중복 감지
def load_seen_ids():
    # 이미 알림을 보낸 트윗 ID 목록 불러오기
    if os.path.exists(SEEN_FILE):
        try:
            with open(SEEN_FILE, 'r') as f:
                return set(json.load(f))
        except json.JSONDecodeError:
            logger.warning("⚠️ seen_tweets.json 파싱 오류. 빈 목록으로 초기화.")
    return set()

def save_seen_ids(ids):
    # 트윗 ID 목록 저장
    try:
        with open(SEEN_FILE, 'w') as f:
            json.dump(list(ids), f)
    except Exception as e:
        logger.error(f"❌ 트윗 ID 저장 실패: {e}")

# 디스코드 전송
def send_discord_alert(username, tweet_id, tag, created_at_kst):
    # 디스코드 웹훅 트윗 알림 전송
    try:
        content = (
            f"🔔 **해시태그 {tag} 트윗 발견!**\n"
            f"작성자: @{username}\n"
            f"작성 시각 (KST): {created_at_kst}\n\n"
            f"https://twitter.com/{username}/status/{tweet_id}"
        )

        payload = {"content": content}
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)

        if response.status_code != 204:
            logger.error(f"❌ 디스코드 전송 실패: {response.status_code} - {response.text}")

    except Exception as e:
        logger.error(f"❌ 디스코드 전송 중 오류: {e}")

def text_crop(text, limit=300):
    return text if len(text) <= limit else text[:limit] + "..."

# 트위터 API 검색
def search_new_tweets(tag, seen_ids):
    # 지정한 해시태그로 새 트윗 검색 및 알림
    new_ids = set()
    url = "https://api.twitter.com/2/tweets/search/recent"
    params = {
        "query": f"{tag} lang:ko -is:retweet",  # 한글, 리트윗 제외
        "max_results": 10,
        "tweet.fields": "author_id,text,id,created_at",
        "expansions": "author_id",
        "user.fields": "username"
    }

    try:
        response = requests.get(url, headers=HEADERS, params=params)
        if response.status_code != 200:
            logger.error(f"❌ Twitter API 요청 실패 ({tag}): {response.status_code} - {response.text}")
            return new_ids

        data = response.json()

        if "data" not in data:
            logger.info(f"ℹ️ '{tag}' 관련 새 트윗 없음.")
            return new_ids

        users = {user["id"]: user["username"] for user in data["includes"]["users"]}

        for tweet in data["data"]:
            tweet_time_utc = datetime.fromisoformat(tweet["created_at"].replace("Z", "+00:00"))
            tweet_time_kst = tweet_time_utc.astimezone(KST)
            if tweet["id"] not in seen_ids and tweet_time_kst > start_time:
                username = users.get(tweet["author_id"], "unknown")
                logger.info(f"📌 새 트윗 감지: @{username} - {tweet['id']} ({tweet_time_kst})")
                send_discord_alert(username, tweet["id"], tag, tweet_time_kst.strftime('%Y-%m-%d %H:%M:%S'))
                new_ids.add(tweet["id"])
            else:
                break

    except Exception as e:
        logger.error(f"❌ '{tag}' 트윗 검색 중 오류: {e}")

    return new_ids

# 메인 루프
if __name__ == "__main__":
    # 주기적으로 해시태그 트윗 검색, 알림 전송
    while True:
        logger.info("🔍 해시태그 모니터링 시작")
        try:
            seen_ids = load_seen_ids()  # 기존에 본 트윗 ID 불러오기
            all_new_ids = set()

            for tag in HASHTAGS:
                logger.info(f"  ▶ {tag} 검색 중...")
                new_ids = search_new_tweets(tag, seen_ids)
                all_new_ids.update(new_ids)

            if all_new_ids:
                seen_ids.update(all_new_ids)
                save_seen_ids(seen_ids)

        except Exception as e:
            logger.error(f"❌ 전체 루프 오류: {e}")

        time.sleep(CHECK_INTERVAL)  # 지정한 주기만큼 대기 후 반복