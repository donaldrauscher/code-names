#!/bin/bash
echo Starting Gunicorn...
gunicorn app:server \
    --name code-names \
    --bind 0.0.0.0:$PORT \
    --workers $GUNICORN_WORKERS \
    --preload \
    --worker-class gevent \
    --timeout 600 \
    --log-level info