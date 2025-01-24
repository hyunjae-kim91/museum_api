#!/bin/bash
# uvicorn app:app --reload /
# uvicorn app:app --reload --host 0.0.0.0 --port 8000
gunicorn app:app --bind 0.0.0.0:8000 -w 5 -k uvicorn.workers.UvicornWorker --timeout 300