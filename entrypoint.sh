#!/bin/sh
gunicorn app:app --bind=:5000 --workers=5 --threads=3
# python3 app.py