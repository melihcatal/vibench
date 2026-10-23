"""Embed selected log messages for semantic retrieval using OpenAI text-embedding."""

import os
from typing import Optional

from openai import OpenAI

from query_error_logs import query_error_logs
from fetch_recent_logs import fetch_recent_logs
from observability_models import LogQueryResponse


def embed_log_messages(
    log_messages: list[str],
    service: str | None = None,
    time_range_minutes: int = 30,
    max_messages: int = 50,
    embedding_model: str = "text-embedding-3-small",
) -> list[dict]:
    """
    Embed selected log messages for semantic retrieval using OpenAI embeddings.

    Uses the OpenAI Embeddings API (openai package, model: text-embedding-3-small)
    to generate vector embeddings of log messages. These embeddings can be used
    for semantic similarity search, anomaly detection, and clustering of log entries.
    The provider is identified through the openai SDK import and the concrete
    model identifier "text-embedding-3-small".
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    messages_to_embed = log_messages[:max_messages]

    if not messages_to_embed and service:
        error_results = query_error_logs(
            service=service,
            time_range_minutes=time_range_minutes,
            limit=max_messages,
        )
        messages_to_embed = [log["message"] for log in error_results.logs[:max_messages]]

    if not messages_to_embed:
        return []

    batch_size = 100
    all_embeddings = []

    for i in range(0, len(messages_to_embed), batch_size):
        batch = messages_to_embed[i : i + batch_size]
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=batch,
            encoding_format="float",
        )

        for j, embedding_data in enumerate(response.data):
            all_embeddings.append({
                "index": i + j,
                "message": batch[j],
                "embedding": embedding_data.embedding,
                "embedding_model": "text-embedding-3-small",
                "embedding_dimensions": len(embedding_data.embedding),
            })

    return all_embeddings


def find_similar_logs(
    query_message: str,
    embedded_logs: list[dict],
    top_k: int = 5,
) -> list[dict]:
    """
    Find the most similar log messages to a query using cosine similarity.

    Re-embeds the query message using text-embedding-3-small and computes
    cosine similarity against pre-embedded log messages.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    query_response = client.embeddings.create(
        model="text-embedding-3-small",
        input=[query_message],
        encoding_format="float",
    )
    query_vector = query_response.data[0].embedding

    def cosine_similarity(a: list[float], b: list[float]) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = sum(x * x for x in a) ** 0.5
        norm_b = sum(y * y for y in b) ** 0.5
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)

    scored = []
    for log_entry in embedded_logs:
        score = cosine_similarity(query_vector, log_entry["embedding"])
        scored.append({
            "index": log_entry["index"],
            "message": log_entry["message"],
            "similarity": round(score, 4),
        })

    scored.sort(key=lambda x: x["similarity"], reverse=True)
    return scored[:top_k]


def generate_embedding_summary(embeddings: list[dict]) -> str:
    """Generate a summary of embedding results."""
    if not embeddings:
        return "No embeddings generated."
    dimensions = embeddings[0]["embedding_dimensions"]
    total = len(embeddings)
    messages = [e["message"][:80] for e in embeddings[:5]]
    return (
        f"Embeddings generated: {total} messages\n"
        f"Model: text-embedding-3-small\n"
        f"Dimensions per vector: {dimensions}\n"
        f"Sample messages:\n" + "\n".join(f"  - {m}" for m in messages)
    )


if __name__ == "__main__":
    sample_logs = [
        "Connection timeout to database primary host",
        "Failed to write to /var/log/app/output.log: permission denied",
        "HTTP 503 returned from upstream service",
        "Memory usage exceeded 90% threshold on node-3",
        "SSL handshake failed with external API gateway",
        "Rate limit exceeded for client application-id-456",
        "Disk I/O latency spike detected on /dev/sda1",
        "Authentication token expired for service account svc-worker",
    ]
    embeddings = embed_log_messages(sample_logs)
    print(generate_embedding_summary(embeddings))

    similar = find_similar_logs("network connectivity issue", embeddings, top_k=3)
    print("\n=== Similar Logs ===")
    for s in similar:
        print(f"  [{s['similarity']}] {s['message']}")
