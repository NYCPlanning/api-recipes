#!/bin/sh
gunicorn app:app --timeout 10000000 --bind=:5000 --workers=5 --threads=4 --log-level=debug --log-file /tmp/log
# python3 app.py