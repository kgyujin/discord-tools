# Discord Tools

| 항목 | 버전/설명 |
| --- | -------- |
| Python | 3.10.12 |

## 디렉터리 구조
```
discord-tools/
├─ bots/
│  └─ voice-chat-detection/
├─ webhooks/
│  └─ x-keyword-notifier/
├─ .gitignore
└─ README.md
```

- **Voice Chat Detection** : [README](./bots/voice-chat-detection/README.md)
- **X Keyword Notifier** : [README](./webhooks/x-keyword-notifier/README.md)

## 실행 방법(과정)

### 일반 실행
1. 프로젝트 폴더 경로 내에서 아래의 명령어를 실행합니다.
```bash
python3 bot.py
```

### Run
1. 프로젝트 폴더 경로 내에서 아래의 명령어 중 하나를 실행합니다.
```bash
bash run.sh
./run.sh
```

### Stop
1. 프로젝트 폴더 경로 내에서 아래의 명령어 중 하나를 실행합니다.
```bash
bash stop.sh
./stop.sh
```

## 참고 명령어
- 봇 작동 여부 확인
```bash
ps aux | grep bot.py
```

- 로그 확인
```bash
cat bot.log
```

- 쉐뱅(./) 사용 시 권한 부여
```bash
chmod +x run.sh
chmod +x stop.sh
```