from __future__ import annotations

import json
import os
from typing import Any

from security_client import safe_fetch


def fetch_db_secret(secret_id: str | None = None) -> dict[str, Any]:
    secret_name = secret_id or os.getenv("SECURITY_DB_SECRET_ID", "database/connection")
    raw = safe_fetch(secret_name)
    data = json.loads(raw)
    return {
        "username": data.get("username"),
        "password": data.get("password"),
        "host": data.get("host"),
        "port": data.get("port"),
        "database": data.get("database"),
        "engine": data.get("engine", "postgres"),
    }
