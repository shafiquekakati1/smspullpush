#!/bin/sh

set -e

exec python3 /app/DandR.py &
exec python3 /app/multireciever.py
