if [ -f ./bot.pid ]; then
  PID=$(cat ./bot.pid)
  echo "[Bot] Stopping X Hashtag Notifier with PID : $PID"
  kill $PID
  rm ./bot.pid
  echo "[Bot] X Hashtag Notifier stopped."
else
  echo "[Bot] not running or PID file is missing."
fi