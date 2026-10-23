"""
log_embedding.py

Embed selected log messages for semantic retrieval using the
OpenAI Embeddings API via the openai SDK.

Required env: OPENAI_API_KEY
"""

import os
from typing import List, Dict, Any
from openai import OpenAI
from observability_models import QueryResponse, LogQueryResult


def embed_log_messages(
    log_results: QueryResponse,
    model: str = "text-embedding-3-small",
    batch_size: int = 100,
) -> List[Dict[str, Any]]:
    """
    Generate vector embeddings for log messages using the OpenAI
    text-embedding-3-small model.

    Args:
        log_results: QueryResponse with log entries to embed.
        model: OpenAI embedding model identifier.
        batch_size: Max messages per API call.

    Returns:
        List of dicts with original message, embedding vector, and metadata.
    """
    api_key = os.environ["OPENAI_API_KEY"]
    client = OpenAI(api_key=api_key)

    messages_with_meta = [
        {"message": r.message, "metadata": {
            "timestamp": r.timestamp,
            "level": r.level,
            "correlation_id": r.correlation_id,
        }}
        for r in log_results.results if r.message and len(r.message) > 0
    ]

    # Deduplicate
    seen = set()
    unique = []
    for item in messages_with_meta:
        if item["message"] not in seen:
            seen.add(item["message"])
            unique.append(item)

    results = []
    for i in range(0, len(unique), batch_size):
        batch = unique[i : i + batch_size]
        texts = [item["message"] for item in batch]

        response = client.embeddings.create(
            input=texts,
            model=model,
        )

        for idx, data in enumerate(response.data):
            results.append({
                "message": batch[idx]["message"],
                "metadata": batch[idx]["metadata"],
                "embedding": data.embedding,
                "model": model,
                "index": i + idx,
            })

    return results


def cosine_similarity(
    vec_a: List[float],
    vec_b: List[float],
) -> float:
    """Compute cosine similarity between two embedding vectors."""
    import math
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    mag_a = math.sqrt(sum(a * a for a in vec_a))
    mag_b = math.sqrt(sum(b * b for b in vec_b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


if __name__ == "__main__":
    from query_error_logs import query_error_logs

    lg = os.environ.get("CLOUDWATCH_LOG_GROUP", "/app/production")
    errors = query_error_logs(
        log_group_name=lg,
        hours_back=2,
        log_level_filter="ERROR",
        limit=20,
    )
    embedded = embed_log_messages(errors)
    print(f"Generated {len(embedded)} embeddings using model {embedded[0]['model']}")
