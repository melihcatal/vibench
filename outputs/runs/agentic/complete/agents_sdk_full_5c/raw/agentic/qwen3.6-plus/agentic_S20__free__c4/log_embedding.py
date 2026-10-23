"""
Embed selected log messages for semantic retrieval.

Uses the OpenAI Embeddings API (api.openai.com) via the openai Python SDK
with the text-embedding-3-small model to generate vector embeddings
for log messages, enabling semantic search and similarity matching.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

import openai
from openai import OpenAI

from observability_models import (
    LogQueryFilter,
    LogEntry,
    QueryResult,
)
from observability_client import query_logs

OPENAI_API_HOST = "https://api.openai.com/v1"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def embed_log_message(
    message: str,
    model: str = OPENAI_EMBEDDING_MODEL,
    dimensions: Optional[int] = None,
) -> Dict[str, Any]:
    """Embed a single log message using OpenAI embeddings.

    Sends the log message to the OpenAI Embeddings API at api.openai.com
    using the text-embedding-3-small model to produce a vector embedding
    suitable for semantic search and similarity comparisons.

    Args:
        message: The log message text to embed.
        model: OpenAI embedding model identifier.
        dimensions: Optional output dimensionality for the embedding vector.

    Returns:
        Dict with embedding vector, model info, and metadata.
    """
    openai_client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY", ""),
        base_url=OPENAI_API_HOST,
    )

    kwargs: Dict[str, Any] = {
        "model": model,
        "input": message,
    }
    if dimensions is not None:
        kwargs["dimensions"] = dimensions

    response = openai_client.embeddings.create(**kwargs)

    embedding_data = response.data[0]
    embedding_vector = embedding_data.embedding

    return {
        "model": model,
        "provider": "openai",
        "provider_endpoint": OPENAI_API_HOST,
        "input_text": message,
        "embedding": embedding_vector,
        "embedding_dimension": len(embedding_vector),
        "usage_tokens": response.usage.total_tokens,
        "model_id": response.model,
    }


def embed_log_messages(
    messages: List[str],
    model: str = OPENAI_EMBEDDING_MODEL,
    dimensions: Optional[int] = None,
) -> Dict[str, Any]:
    """Embed multiple log messages in a single batch via OpenAI.

    Sends a batch of log messages to the OpenAI Embeddings API
    (api.openai.com) using text-embedding-3-small for vectorization.

    Args:
        messages: List of log message texts to embed.
        model: OpenAI embedding model identifier.
        dimensions: Optional output dimensionality for embedding vectors.

    Returns:
        Dict with batch embedding results.
    """
    if not messages:
        return {
            "model": model,
            "provider": "openai",
            "provider_endpoint": OPENAI_API_HOST,
            "embeddings": [],
            "total_embedded": 0,
        }

    openai_client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY", ""),
        base_url=OPENAI_API_HOST,
    )

    kwargs: Dict[str, Any] = {
        "model": model,
        "input": messages,
    }
    if dimensions is not None:
        kwargs["dimensions"] = dimensions

    response = openai_client.embeddings.create(**kwargs)

    embeddings = []
    for item in response.data:
        embeddings.append({
            "index": item.index,
            "embedding": item.embedding,
            "embedding_dimension": len(item.embedding),
        })

    return {
        "model": model,
        "provider": "openai",
        "provider_endpoint": OPENAI_API_HOST,
        "embeddings": embeddings,
        "total_embedded": len(embeddings),
        "usage_tokens": response.usage.total_tokens,
        "model_id": response.model,
    }


def embed_recent_error_logs(
    service: Optional[str] = None,
    time_window_minutes: int = 30,
    limit: int = 20,
    model: str = OPENAI_EMBEDDING_MODEL,
    dimensions: Optional[int] = None,
) -> Dict[str, Any]:
    """Fetch recent error logs from Datadog and embed their messages.

    Queries api.datadoghq.com via the datadog-api-client SDK for recent
    error logs, then generates embeddings using OpenAI text-embedding-3-small
    for semantic retrieval and similarity-based log analysis.
    """
    now = datetime.now(timezone.utc)
    time_from = now - timedelta(minutes=time_window_minutes)

    filter_fields = {"status": "error"}
    if service:
        filter_fields["service"] = service

    filter_query = LogQueryFilter(
        query="status:error",
        time_from=time_from,
        time_to=now,
        limit=limit,
        filter_fields=filter_fields,
    )

    log_result: QueryResult = query_logs(filter_query)

    messages = []
    entry_map = []
    for entry in log_result.entries:
        if entry.message:
            messages.append(entry.message)
            entry_map.append({
                "log_id": entry.id,
                "timestamp": entry.timestamp,
                "service": entry.service,
                "status": entry.status,
                "correlation_id": entry.correlation_id,
            })

    if not messages:
        return {
            "model": model,
            "provider": "openai",
            "source": "datadog",
            "log_query": log_result.query_string,
            "embeddings": [],
            "total_embedded": 0,
        }

    embedding_result = embed_log_messages(
        messages=messages,
        model=model,
        dimensions=dimensions,
    )

    enriched_embeddings = []
    for emb in embedding_result["embeddings"]:
        enriched = {**emb}
        if emb["index"] < len(entry_map):
            enriched["log_metadata"] = entry_map[emb["index"]]
            enriched["log_message"] = messages[emb["index"]]
        enriched_embeddings.append(enriched)

    return {
        "model": model,
        "provider": "openai",
        "source": "datadog",
        "log_query": log_result.query_string,
        "total_log_entries": len(log_result.entries),
        "total_embedded": len(enriched_embeddings),
        "embeddings": enriched_embeddings,
        "usage_tokens": embedding_result.get("usage_tokens", 0),
    }


def main() -> None:
    """CLI entry point for embedding log messages."""
    message = os.environ.get("LOG_MESSAGE", "Database connection pool exhausted")
    model = os.environ.get("OPENAI_EMBEDDING_MODEL", OPENAI_EMBEDDING_MODEL)
    dimensions = os.environ.get("EMBEDDING_DIMENSIONS", None)
    dims = int(dimensions) if dimensions else None

    result = embed_log_message(
        message=message,
        model=model,
        dimensions=dims,
    )
    output = {k: v for k, v in result.items() if k != "embedding"}
    output["embedding_preview"] = (
        result["embedding"][:5] + ["..."] if result["embedding"] else []
    )
    print(json.dumps(output, indent=2, default=str))


if __name__ == "__main__":
    main()
