echo "[Bot] X Hashtag Notifier Running"
nohup python3 ./main.py > ./logs/hashtag.log 2>&1 &
echo $! > ./bot.pid
echo "[Bot] Run X Hashtag Notifier with PID : $(cat ./bot.pid)"