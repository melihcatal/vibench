"""Embed selected log messages for semantic retrieval using OpenAI Embeddings API."""

import json
import os
from typing import List, Optional

import openai
from openai import OpenAI

from observability_models import LogEntry


def embed_log_messages(
    log_messages: List[str],
    model: str = "text-embedding-3-small",
    api_key: Optional[str] = None,
    dimensions: Optional[int] = None,
) -> dict:
    """Embed selected log messages for semantic retrieval using OpenAI Embeddings API.

    Uses the OpenAI SDK (openai) with OPENAI_API_KEY for authentication.
    The concrete model is text-embedding-3-small from the OpenAI embeddings
    model family.
    """
    client = OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))

    params = {
        "model": model,
        "input": log_messages,
    }
    if dimensions is not None:
        params["dimensions"] = dimensions

    response = client.embeddings.create(**params)

    embeddings_data = []
    for i, data in enumerate(response.data):
        embeddings_data.append({
            "index": i,
            "text_preview": log_messages[i][:100],
            "embedding_dimension": len(data.embedding),
            "embedding": data.embedding,
        })

    return {
        "provider": "OpenAI Embeddings",
        "model": model,
        "messages_embedded": len(log_messages),
        "embedding_dimension": embeddings_data[0]["embedding_dimension"] if embeddings_data else 0,
        "embeddings": embeddings_data,
        "usage": {
            "prompt_tokens": response.usage.prompt_tokens,
            "total_tokens": response.usage.total_tokens,
        },
    }


def embed_log_entries(
    log_entries: List[LogEntry],
    model: str = "text-embedding-3-small",
    api_key: Optional[str] = None,
) -> dict:
    """Extract messages from log entries and embed them for semantic retrieval."""
    messages = [str(entry.message) for entry in log_entries if entry.message]
    return embed_log_messages(messages, model=model, api_key=api_key)


def main():
    sample_messages = [
        "Database connection pool exhausted: maximum connections reached for db-primary",
        "HTTP 503 Service Unavailable: payment-gateway health check failed",
        "Circuit breaker OPEN for downstream auth-service after 5 consecutive failures",
        "Memory usage exceeded 90% threshold on pod worker-7 in namespace production",
    ]

    result = embed_log_messages(
        sample_messages,
        model="text-embedding-3-small",
    )
    # Truncate embeddings for display
    for emb in result["embeddings"]:
        emb["embedding"] = emb["embedding"][:10] + ["..."]
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
