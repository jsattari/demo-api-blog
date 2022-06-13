#!/bin/zsh
export FLASK_APP=./api/main.py
source venv/bin/activate
flask run -h 0.0.0.0