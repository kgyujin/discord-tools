echo "[Bot] Voice Chat Detection Running"
nohup python3 ./bot.py > ./bot.log 2>&1 &
echo $! > ./bot.pid
echo "[Bot] Run Voice Chat Detection with PID : $(cat ./bot.pid)"