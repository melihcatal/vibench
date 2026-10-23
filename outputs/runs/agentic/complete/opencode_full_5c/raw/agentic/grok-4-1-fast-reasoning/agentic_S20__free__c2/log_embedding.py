import os
from openai import OpenAI
from datetime import datetime, timedelta
from typing import List, Dict, Any
from observability_client import ObservabilityClient


def log_embedding(hours_back: int = 1) -> List[Dict[str, Any]]:
    client = ObservabilityClient()
    now = datetime.utcnow()
    to_ts = int(now.timestamp() * 1000)
    from_ts = int((now - timedelta(hours=hours_back)).timestamp() * 1000)
    logs = client.query_logs("status:error", from_ts, to_ts, 10)

    embed_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    messages = [
        log.get("attributes", {}).get("message", "")
        for log in logs
        if log.get("attributes", {}).get("message")
    ]
    messages = [m for m in messages if m]

    if not messages:
        return []

    response = embed_client.embeddings.create(
        input=messages, model="text-embedding-3-small"
    )

    embeddings = []
    for i, emb in enumerate(response.data):
        embeddings.append(
            {
                "log_index": i,
                "message": messages[i],
                "embedding": emb.embedding[:10] + ["..."],  # truncated
            }
        )

    return embeddings
