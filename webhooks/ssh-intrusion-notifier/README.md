# SSH Intrusion Notifier

## 기능
| 기능 | 설명 |
|------|------|
| SSH 침입 감지 | `/var/log/auth.log`를 실시간 감시하여 침입 시도 탐지 |
| 디스코드 알림 | 감지된 침입 시도를 지정한 디스코드 웹훅으로 전송 |
| 키워드 기반 필터링 | `"Failed password"`, `"Invalid user"` 등 지정된 키워드 감시 |
| 로그 기록 | 감지된 침입 내역을 `intrusion.log`에 기록 |

## 구조
```
ssh-intrusion-notifier/
├─ .env
├─ intrusion.log
├─ main.py
├─ README.md
├─ requirements.txt
├─ run.sh
└─ stop.sh
```

## 환경 변수(.env) 설정
```env
DISCORD_WEBHOOK_URL=디스코드_웹훅_URL
AUTH_LOG_PATH=/var/log/auth.log
KEYWORDS=Failed password,Invalid user
IGNORE_KEYWORDS=preauth
CHECK_INTERVAL=2
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
- 기본 감시 대상 로그 파일은 /var/log/auth.log이며, 필요 시 .env에서 경로를 변경할 수 있습니다.
- KEYWORDS에 지정된 문자열이 로그에 감지되면 웹훅으로 알림을 전송합니다.
- 
알림은 intrusion.log에도 저장되어 서버 접근 기록을 추적할 수 있습니다.
- 시스템에 따라 sudo 권한이 필요할 수 있습니다.