"""Embed selected log messages for semantic retrieval using OpenAI Embeddings and Datadog.

Provider (log query): Datadog Logs API v2
- Endpoint: POST https://api.datadoghq.com/api/v2/logs/events/search
- SDK: datadog-api-client (datadog_api_client.v2.api.logs_api.LogsApi)

Provider (embeddings): OpenAI Embeddings API
- Model: text-embedding-3-small
- Endpoint: https://api.openai.com/v1/embeddings
- SDK: openai
"""

import os
import json
from typing import Optional

from openai import OpenAI
from fetch_recent_logs import fetch_recent_logs
from observability_models import LogQueryResponse
from observability_client import DatadogObservabilityClient


OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def embed_log_messages(
    service: str,
    hours: int = 1,
    limit: int = 50,
    client: Optional[DatadogObservabilityClient] = None,
    openai_client: Optional[OpenAI] = None,
) -> list[dict]:
    """Fetch log messages from Datadog and generate embeddings for semantic retrieval.

    Steps:
    1. Fetch recent logs from Datadog Logs API v2 for the given service.
    2. Extract log message text from entries.
    3. Generate embeddings using OpenAI text-embedding-3-small model.
    4. Return messages paired with their embedding vectors and metadata.

    Reference: https://platform.openai.com/docs/api-reference/embeddings

    Args:
        service: The service name to fetch logs for.
        hours: Number of recent hours to search.
        limit: Maximum number of log entries to embed.
        client: Optional pre-configured DatadogObservabilityClient.
        openai_client: Optional pre-configured OpenAI client.

    Returns:
        List of dicts with original message, embedding vector, and metadata.
    """
    if openai_client is None:
        openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))

    response: LogQueryResponse = fetch_recent_logs(
        service=service,
        hours=hours,
        limit=limit,
        client=client,
    )

    messages = []
    for log in response.logs:
        msg_text = log.get("message", "").strip()
        if msg_text:
            messages.append({
                "timestamp": log.get("date", ""),
                "message": msg_text,
                "service": log.get("service", ""),
                "status": log.get("status", ""),
                "hostname": log.get("hostname", ""),
            })

    if not messages:
        return []

    embeddings = _batch_embed(openai_client, messages)
    return embeddings


def _batch_embed(
    openai_client: OpenAI,
    messages: list[dict],
) -> list[dict]:
    """Generate embeddings for a batch of log messages using OpenAI text-embedding-3-small.

    The OpenAI Embeddings API supports batch input up to 2048 messages per request.
    """
    input_texts = [entry["message"] for entry in messages]

    response = openai_client.embeddings.create(
        model=OPENAI_EMBEDDING_MODEL,
        input=input_texts,
        encoding_format="float",
    )

    results = []
    for i, entry in enumerate(messages):
        embedding_obj = response.data[i]
        results.append({
            "message": entry["message"],
            "embedding": embedding_obj.embedding,
            "embedding_dimension": len(embedding_obj.embedding),
            "model": OPENAI_EMBEDDING_MODEL,
            "timestamp": entry["timestamp"],
            "service": entry["service"],
            "status": entry.get("status", ""),
            "hostname": entry.get("hostname", ""),
        })
    return results


def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """Compute cosine similarity between two embedding vectors."""
    import math
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def find_similar_logs(
    query_text: str,
    embedded_logs: list[dict],
    top_k: int = 5,
    openai_client: Optional[OpenAI] = None,
) -> list[dict]:
    """Find log messages most similar to a query using embedding cosine similarity.

    Args:
        query_text: The search query text.
        embedded_logs: List of log entries with pre-computed embeddings.
        top_k: Number of top results to return.
        openai_client: Optional pre-configured OpenAI client for query embedding.

    Returns:
        List of log entries sorted by similarity score, with scores attached.
    """
    if openai_client is None:
        openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))

    query_embedding_resp = openai_client.embeddings.create(
        model=OPENAI_EMBEDDING_MODEL,
        input=query_text,
        encoding_format="float",
    )
    query_vec = query_embedding_resp.data[0].embedding

    scored = []
    for entry in embedded_logs:
        score = cosine_similarity(query_vec, entry["embedding"])
        scored.append({**entry, "similarity_score": score})

    scored.sort(key=lambda x: x["similarity_score"], reverse=True)
    return scored[:top_k]


def main():
    """Entry point for embedding log messages."""
    service = os.environ.get("LOG_SERVICE", "web-api")
    hours = int(os.environ.get("EMBED_HOURS", "1"))

    results = embed_log_messages(service=service, hours=hours)

    # Print summary without full embedding vectors for readability
    summary = []
    for r in results:
        summary.append({
            "message": r["message"],
            "embedding_dimension": r["embedding_dimension"],
            "model": r["model"],
            "timestamp": r["timestamp"],
            "service": r["service"],
            "status": r["status"],
        })
    print(json.dumps(summary, indent=2, default=str))


if __name__ == "__main__":
    main()
