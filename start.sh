#!/bin/bash
cd /app

find /app -name "*.session-journal" -delete 2>/dev/null
find /app -name "*.session-wal" -delete 2>/dev/null

git fetch origin Yato
git reset --hard origin/Yato

mkdir -p /app/downloads

pip install -r requirements.txt -q
python main.py
