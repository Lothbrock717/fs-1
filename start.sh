#!/bin/bash
cd /app
git fetch origin Yato
git reset --hard origin/Yato
cp /config.py /app/config.py
pip install -r requirements.txt -q
python main.py
