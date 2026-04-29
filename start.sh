#!/bin/bash
cd /app

# Clean stale session locks
find /app -name "*.session-journal" -delete 2>/dev/null
find /app -name "*.session-wal" -delete 2>/dev/null

git fetch origin Yato
git reset --hard origin/Yato

# Restore config from mount since git reset overwrites it
if [ -f /app/config.py.mounted ]; then
  cp /app/config.py.mounted /app/config.py
fi

pip install -r requirements.txt -q
python main.py
