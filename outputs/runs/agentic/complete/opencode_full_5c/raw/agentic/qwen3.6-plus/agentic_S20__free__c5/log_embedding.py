import os
import json
from typing import Any

import requests

from observability_models import LogEntry


OPENAI_API_URL = "https://api.openai.com/v1/embeddings"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def get_openai_api_key() -> str:
    key = os.environ.get("OPENAI_API_KEY", "")
    if not key:
        raise RuntimeError("OPENAI_API_KEY environment variable is required")
    return key


def embed_log_messages(
    log_entries: list[LogEntry],
) -> list[dict[str, Any]]:
    texts = []
    for entry in log_entries:
        text = f"[{entry.status}] {entry.message}"
        if entry.attributes:
            text += f" {json.dumps(entry.attributes)}"
        texts.append(text)

    if not texts:
        return []

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {get_openai_api_key()}",
    }

    payload = {
        "model": OPENAI_EMBEDDING_MODEL,
        "input": texts,
    }

    resp = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    result = resp.json()

    embeddings = []
    for item in result.get("data", []):
        idx = item.get("index", 0)
        entry = log_entries[idx] if idx < len(log_entries) else None
        embeddings.append(
            {
                "log_id": entry.id if entry else "",
                "model": OPENAI_EMBEDDING_MODEL,
                "embedding": item.get("embedding", []),
                "status": entry.status if entry else "",
                "service": entry.service if entry else "",
                "timestamp": entry.timestamp if entry else "",
            }
        )

    return embeddings


if __name__ == "__main__":
    sample_entries = [
        LogEntry(
            id="log-e01",
            message="Connection pool exhausted",
            status="error",
            service="db-proxy",
            hostname="prod-db-01",
            timestamp="2025-01-15T10:23:01Z",
            attributes={"pool_size": 50, "active_connections": 50},
        ),
        LogEntry(
            id="log-e02",
            message="Request timeout after 30s",
            status="error",
            service="api-gateway",
            hostname="prod-gw-03",
            timestamp="2025-01-15T10:23:15Z",
            attributes={"endpoint": "/api/orders", "timeout_ms": 30000},
        ),
        LogEntry(
            id="log-e03",
            message="Cache miss for key user:profile:42",
            status="warning",
            service="cache-layer",
            hostname="prod-cache-01",
            timestamp="2025-01-15T10:23:20Z",
            attributes={"cache_key": "user:profile:42", "ttl_remaining": 0},
        ),
    ]
    embeddings = embed_log_messages(sample_entries)
    for emb in embeddings:
        print(
            json.dumps(
                {
                    "log_id": emb["log_id"],
                    "model": emb["model"],
                    "embedding_dim": len(emb["embedding"]),
                    "status": emb["status"],
                    "service": emb["service"],
                },
                indent=2,
            )
        )
