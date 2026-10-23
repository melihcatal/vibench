import os
from collections import Counter
from typing import Any

import requests

AUDIT_API_BASE = os.environ.get("MONGODB_ATLAS_DATA_API_BASE", "https://data.mongodb-api.com/app")
DATA_API_KEY = os.environ.get("MONGODB_DATA_API_KEY", "")
DATA_SOURCE = os.environ.get("MONGODB_DATA_SOURCE", "Cluster0")
DATABASE = os.environ.get("MONGODB_DATABASE", "identity")
COLLECTION = os.environ.get("MONGODB_AUDIT_COLLECTION", "audit_events")


def summarize_audit_events(limit: int = 100) -> dict[str, Any]:
    url = f"{AUDIT_API_BASE.rstrip('/')}/data/v1/action/find"
    headers = {"Content-Type": "application/json", "api-key": DATA_API_KEY}
    payload = {"dataSource": DATA_SOURCE, "database": DATABASE, "collection": COLLECTION, "limit": limit}
    response = requests.post(url, json=payload, headers=headers, timeout=20)
    response.raise_for_status()
    docs = response.json().get("documents", [])
    providers = Counter(doc.get("provider", "unknown") for doc in docs)
    outcomes = Counter(doc.get("outcome", "unknown") for doc in docs)
    return {"count": len(docs), "by_provider": dict(providers), "by_outcome": dict(outcomes), "documents": docs}
