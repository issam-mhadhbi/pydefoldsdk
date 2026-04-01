if [ ! -d \".venv\" ]; then python3 -m venv .venv && echo '.venv created'; else echo '.venv exists'; fi
# .venv/bin/pip install -r requirements.txt
