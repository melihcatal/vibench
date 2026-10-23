import os
from datetime import datetime, timezone
from typing import Any

import requests

AUDIT_API_BASE = os.environ.get("MONGODB_ATLAS_DATA_API_BASE", "https://data.mongodb-api.com/app")
DATA_API_KEY = os.environ.get("MONGODB_DATA_API_KEY", "")
DATA_SOURCE = os.environ.get("MONGODB_DATA_SOURCE", "Cluster0")
DATABASE = os.environ.get("MONGODB_DATABASE", "identity")
COLLECTION = os.environ.get("MONGODB_AUDIT_COLLECTION", "audit_events")


def persist_login_audit(record: dict[str, Any]) -> dict[str, Any]:
    url = f"{AUDIT_API_BASE.rstrip('/')}/data/v1/action/insertOne"
    headers = {"Content-Type": "application/json", "api-key": DATA_API_KEY}
    document = dict(record)
    document.setdefault("created_at", datetime.now(timezone.utc).isoformat())
    payload = {"dataSource": DATA_SOURCE, "database": DATABASE, "collection": COLLECTION, "document": document}
    response = requests.post(url, json=payload, headers=headers, timeout=20)
    response.raise_for_status()
    return response.json()
