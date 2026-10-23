import os
from typing import Optional

import openai

from observability_models import LogEntry
from fetch_recent_logs import fetch_recent_logs

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"

openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)


def embed_log_message(
    text: str,
    model: str = OPENAI_EMBEDDING_MODEL,
) -> list[float]:
    response = openai_client.embeddings.create(
        model=model,
        input=text,
    )
    return response.data[0].embedding


def embed_log_messages(
    texts: list[str],
    model: str = OPENAI_EMBEDDING_MODEL,
) -> list[list[float]]:
    if not texts:
        return []
    response = openai_client.embeddings.create(
        model=model,
        input=texts,
    )
    sorted_data = sorted(response.data, key=lambda d: d.index)
    return [d.embedding for d in sorted_data]


def embed_recent_logs(
    service: str = "",
    hours: int = 1,
    limit: int = 50,
) -> list[dict]:
    query_result = fetch_recent_logs(service=service, hours=hours, limit=limit)
    messages = [entry.message for entry in query_result.entries]
    embeddings = embed_log_messages(messages) if messages else []
    results: list[dict] = []
    for entry, embedding in zip(query_result.entries, embeddings):
        results.append(
            {
                "log_id": entry.id,
                "timestamp": entry.timestamp.isoformat(),
                "service": entry.service,
                "message": entry.message,
                "embedding": embedding,
                "embedding_dimension": len(embedding),
                "model": OPENAI_EMBEDDING_MODEL,
            }
        )
    return results


if __name__ == "__main__":
    result = embed_log_message(
        "Connection refused to upstream service at 10.0.1.5:8080"
    )
    print(f"Embedding dimension: {len(result)}")
    print(f"First 5 values: {result[:5]}")
