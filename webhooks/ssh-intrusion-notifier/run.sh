#!/bin/bash
echo "[Bot] SSH 침입 감시 봇 실행"
nohup python3 main.py > intrusion.log 2>&1 &
echo $! > bot.pid
echo "[Bot] PID: $(cat bot.pid)"