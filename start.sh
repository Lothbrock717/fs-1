git pull origin $(git rev-parse --abbrev-ref HEAD) 2>/dev/null || echo "Git pull skipped"
pip install -r requirements.txt --no-cache-dir
python3 main.py
