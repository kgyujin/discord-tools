# X Hashtag Notifier

## 기능
| 기능 | 설명 |
| --- | --- |
| 해시태그 트윗 감지 | 지정한 해시태그가 포함된 새 트윗을 실시간으로 감지 |
| 디스코드 알림 | 감지된 트윗 정보를 지정한 디스코드 웹훅으로 전송 |
| 중복 방지 | 이미 알림을 보낸 트윗은 다시 알리지 않음 |
| 데이터 영속화 | 감지한 트윗 ID를 JSON 파일로 저장/복원 |

## 구조
```
x-hashtag-notifier/
├─ .env
├─ hashtag.log
├─ main.py
├─ README.md
├─ requirements.txt
├─ run.sh
├─ seen_tweets.json
└─ stop.sh
```

## 환경 변수(.env) 설정
```env
TWITTER_BEARER_TOKEN=트위터_API_베어러_토큰
DISCORD_WEBHOOK_URL=디스코드_웹훅_URL
MONITOR_HASHTAGS=#해시태그1,#해시태그2
SEEN_FILE=seen_tweets.json
CHECK_INTERVAL=60
```

## 사용 방법
1. `.env` 파일에 환경 변수 설정  
2. 의존성 설치  
   ```bash
   pip install -r requirements.txt
   ```
3. 봇 실행  
   아래의 명령어 중 하나를 실행합니다.
   ```bash
   python3 main.py
   bash run.sh
   ./run.sh
   ```

4. 봇 중지  
   아래의 명령어 중 하나를 실행합니다.
   ```bash
   bash stop.sh
   ./stop.sh
   ```

## 참고
- 봇이 정상적으로 동작하려면 트위터 API 토큰과 디스코드 웹훅 URL이 필요합니다.
- 감지한 트윗 ID는 `seen_tweets.json` 파일에 저장되어 중복 알림을 방지합니다.
- 로그는 `hashtags.log` 파일에 기록됩니다.
- 감지 대상 해시태그는 환경 변수(.env)의 `MONITOR_HASHTAGS`에서 수정할 수 있습니다.