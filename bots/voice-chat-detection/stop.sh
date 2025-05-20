if [ -f ./bot.pid ]; then
  PID=$(cat ./bot.pid)
  echo "[Bot] Stopping Voice Chat Detection with PID : $PID"
  kill $PID
  rm ./bot.pid
  echo "[Bot] Voice Chat Detection stopped."
else
  echo "[Bot] not running or PID file is missing."
fi