#!/bin/bash
cp /config.py /app/config.py
cd /app
pip install -r requirements.txt -q
cp /config.py /app/config.py
python main.py
