#!/bin/bash
cp /config.py /app/config.py
cd /app
git fetch origin Yato
git reset --hard origin/Yato
cp /config.py /app/config.py
pip install -r requirements.txt -q
cp /config.py /app/config.py
python main.py
