#!/bin/bash
cd /app
git pull origin Yato
pip install -r requirements.txt -q
python main.py
