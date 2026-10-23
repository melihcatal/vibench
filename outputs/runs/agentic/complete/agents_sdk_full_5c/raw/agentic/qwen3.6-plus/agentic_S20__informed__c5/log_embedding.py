"""Embed selected log messages for semantic retrieval using OpenAI Embeddings API."""

import json
import os
from typing import Optional

from openai import OpenAI

from query_error_logs import query_error_logs


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")


def embed_log_message(
    message: str,
    model: str = "text-embedding-3-small",
) -> list[float]:
    """Generate an embedding vector for a single log message using OpenAI text-embedding-3-small.

    Uses the OpenAI embeddings API to produce a dense vector suitable for
    semantic similarity search and clustering of log entries.
    """
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=message,
    )
    return response.data[0].embedding


def embed_log_messages(
    messages: list[str],
    model: str = "text-embedding-3-small",
) -> list[dict]:
    """Batch embed multiple log messages using OpenAI Embeddings API.

    Returns a list of dicts pairing each original message with its embedding vector.
    """
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=messages,
    )
    return [
        {
            "message": msg,
            "embedding": item.embedding,
        }
        for msg, item in zip(messages, response.data)
    ]


def embed_recent_error_logs(
    service: str,
    environment: str = "production",
    minutes_ago: int = 60,
    max_logs: int = 20,
) -> list[dict]:
    """Fetch recent error logs and embed them for semantic retrieval.

    Uses OpenAI text-embedding-3-small model to generate embeddings for
    error log messages from the Datadog Logs API.
    """
    error_logs = query_error_logs(
        service=service,
        environment=environment,
        minutes_ago=minutes_ago,
        limit=max_logs,
    )

    messages = [log.get("message", "") for log in error_logs if log.get("message")]
    if not messages:
        return []

    return embed_log_messages(messages)


if __name__ == "__main__":
    embeddings = embed_recent_error_logs(
        service="payment-api",
        environment="production",
        minutes_ago=30,
        max_logs=10,
    )
    for item in embeddings:
        print(json.dumps({
            "message": item["message"],
            "embedding_dim": len(item["embedding"]),
            "embedding_preview": item["embedding"][:5],
        }, indent=2))
