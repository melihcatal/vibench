import os
from typing import Any, Dict

import httpx


def login_audit_store(record: Dict[str, Any]) -> Dict[str, Any]:
    url = os.environ.get("MONGODB_DATA_API_URL", "")
    api_key = os.environ.get("MONGODB_DATA_API_KEY", "")
    response = httpx.post(
        url,
        headers={"Api-Key": api_key, "Content-Type": "application/json"},
        json={"dataSource": os.environ.get("MONGODB_DATA_SOURCE", "Cluster0"), "database": os.environ.get("MONGODB_DATABASE", "identity"), "collection": os.environ.get("MONGODB_COLLECTION", "login_audit"), "document": record},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
