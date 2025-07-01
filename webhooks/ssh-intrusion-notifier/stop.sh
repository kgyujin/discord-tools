#!/bin/bash
if [ -f bot.pid ]; then
  PID=$(cat bot.pid)
  echo "[Bot] 종료 중... PID: $PID"
  kill $PID
  rm bot.pid
else
  echo "[Bot] 봇이 실행 중이지 않거나 PID 파일이 없습니다."
fi