#!/bin/sh
set -eu

MODE="${1:-web}"

wait_for_postgres() {
  python - <<'PY'
import os
import socket
import time

host = os.environ.get("DATABASE_HOST", "postgres")
port = int(os.environ.get("DATABASE_PORT", "5432"))
timeout_seconds = int(os.environ.get("DATABASE_WAIT_TIMEOUT", "60"))
deadline = time.time() + timeout_seconds

while True:
    try:
        with socket.create_connection((host, port), timeout=2):
            print(f"Postgres is reachable at {host}:{port}")
            break
    except OSError as exc:
        if time.time() >= deadline:
            raise SystemExit(f"Timed out waiting for Postgres at {host}:{port}: {exc}")
        print(f"Waiting for Postgres at {host}:{port}: {exc}")
        time.sleep(2)
PY
}

run_migrations() {
  cd /app
  uv run alembic upgrade head
}

wait_for_postgres
run_migrations

if [ "$MODE" = "migrate-only" ]; then
  exit 0
fi

cd /app/src
exec uv run uvicorn main:app --host 0.0.0.0 --port "${APP_PORT:-8000}" --proxy-headers
