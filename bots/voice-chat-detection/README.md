# Voice Chat Detection

## 기능
| 기능 | 설명 |
| --- | --- |
| 음성 채널 참가 감지 | 사용자가 음성 채널에 참가하면 지정된 텍스트 채널에 알림 메시지 전송 |
| 음성 채널 퇴장 감지 | 사용자가 음성 채널에서 나가면 참가/퇴장 시간 및 통화 시간 포함 알림 메시지 수정 |
| 데이터 영속화 | 음성 채널 참가 정보를 JSON 파일로 저장/복원 |

## 구조
```
voice-chat-detection/
├─ .env
├─ bot.log
├─ bot.pid
├─ bot.py
├─ README.md
├─ requirements.txt
├─ run.sh
├─ stop.sh
└─ voice_data.json
```

## 환경 변수(.env) 설정
```env
DISCORD_BOT_TOKEN=MA...
VOICE_ALERT_CHANNEL=voice-room
VOICE_DATA_FILE=voice_data.json
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
   python3 bot.py
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
- 봇이 정상적으로 동작하려면 디스코드 봇 토큰과 알림을 보낼 텍스트 채널이 필요합니다.
- 음성 데이터는 `voice_data.json` 파일에 자동 저장되며, 이는 환경 변수를 통해 지정할 수 있습니다.
- 로그는 `bot.log` 파일에 기록됩니다.