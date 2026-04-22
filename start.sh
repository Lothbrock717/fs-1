#!/bin/bash
cd /app
git fetch origin Yato
git reset --hard origin/Yato
pip install -r requirements.txt -q
python main.py
