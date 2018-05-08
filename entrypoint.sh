#!/bin/bash

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn app:server \
    --name code-names \
    --bind 0.0.0.0:$PORT \
    --workers 3 \
    --preload \
    --worker-class gevent \
    --timeout 600 \
    --log-level=info \
    "$@"