"""
Embeds selected log messages for semantic retrieval.

Uses the OpenAI Embeddings API (api.openai.com) via the openai SDK
to generate dense vector embeddings for log messages.
Auth: OPENAI_API_KEY environment variable.
"""

import json
import math
import os
from typing import Optional

from openai import OpenAI

OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def embed_log_messages(
    messages: list[dict],
    model: str = OPENAI_EMBEDDING_MODEL,
    dimensions: Optional[int] = None,
) -> list[dict]:
    """Embed log messages using the OpenAI Embeddings API.

    Calls api.openai.com via the openai Python SDK using the
    text-embedding-3-small model to generate dense vector embeddings
    for each log message's text content.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    texts = [entry.get("message", "") for entry in messages]

    kwargs: dict = {"input": texts, "model": model}
    if dimensions:
        kwargs["dimensions"] = dimensions

    response = client.embeddings.create(**kwargs)

    results = []
    for idx, embedding_data in enumerate(response.data):
        entry = messages[idx].copy() if idx < len(messages) else {}
        results.append({
            "original": entry,
            "embedding": embedding_data.embedding,
            "embedding_model": model,
            "embedding_index": embedding_data.index,
            "embedding_dimensions": len(embedding_data.embedding),
        })

    return results


def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """Compute cosine similarity between two vectors."""
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


def find_similar_logs(
    embedded_logs: list[dict],
    query_text: str,
    query_embedding: list[float],
    top_k: int = 3,
) -> list[dict]:
    """Find the most similar log messages to a query using cosine similarity.

    Computes cosine similarity between the query embedding and each
    log message embedding to perform semantic retrieval.
    """
    scored = []
    for entry in embedded_logs:
        sim = cosine_similarity(query_embedding, entry["embedding"])
        scored.append({
            "similarity": sim,
            "log_entry": entry["original"],
            "embedding_model": entry["embedding_model"],
        })

    scored.sort(key=lambda x: x["similarity"], reverse=True)
    return scored[:top_k]


def embed_and_find_similar(
    messages: list[dict],
    query_text: str,
    model: str = OPENAI_EMBEDDING_MODEL,
    top_k: int = 3,
) -> list[dict]:
    """Embed log messages and a query, then return the most similar matches.

    Uses the OpenAI text-embedding-3-small model on api.openai.com
    to embed both the log messages and the query text, then ranks
    messages by cosine similarity for semantic log retrieval.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    # Embed log messages
    texts = [entry.get("message", "") for entry in messages]
    response = client.embeddings.create(input=texts, model=model)

    embedded = []
    for idx, emb in enumerate(response.data):
        entry = messages[idx].copy() if idx < len(messages) else {}
        embedded.append({
            "original": entry,
            "embedding": emb.embedding,
            "embedding_model": model,
            "embedding_index": emb.index,
            "embedding_dimensions": len(emb.embedding),
        })

    # Embed query
    query_response = client.embeddings.create(input=[query_text], model=model)
    query_embedding = query_response.data[0].embedding

    # Rank by similarity
    return find_similar_logs(embedded, query_text, query_embedding, top_k)


def format_embedding_report(
    embedded_logs: list[dict],
    include_vectors: bool = False,
) -> str:
    """Format a human-readable embedding report."""
    lines = [
        "Log Message Embedding Report (OpenAI Embeddings API)",
        "=" * 55,
        f"Messages embedded: {len(embedded_logs)}",
        "",
    ]

    for i, entry in enumerate(embedded_logs, 1):
        original = entry.get("original", {})
        dims = entry.get("embedding_dimensions", 0)
        lines.append(f"[{i}] Service: {original.get('service', 'unknown')}")
        lines.append(f"    Message: {original.get('message', '')}")
        lines.append(f"    Model: {entry.get('embedding_model', 'unknown')}")
        lines.append(f"    Dimensions: {dims}")
        if include_vectors and entry.get("embedding"):
            vec_preview = entry["embedding"][:5]
            lines.append(f"    Vector preview: [{', '.join(f'{v:.4f}' for v in vec_preview)}...]")
        lines.append("")

    lines.append("=" * 55)
    return "\n".join(lines)


def main():
    """Entry point for embedding log messages and semantic retrieval."""
    sample_messages = [
        {
            "message": "Connection pool exhausted after 100 concurrent database connections",
            "timestamp": "2025-01-15T10:00:00Z",
            "service": "database-service",
            "status": "error",
        },
        {
            "message": "SSL certificate renewal completed for api.example.com",
            "timestamp": "2025-01-15T10:05:00Z",
            "service": "certificate-manager",
            "status": "info",
        },
        {
            "message": "Rate limit exceeded for client IP 192.168.1.100 on endpoint /api/v2/users",
            "timestamp": "2025-01-15T10:10:00Z",
            "service": "api-gateway",
            "status": "warning",
        },
        {
            "message": "Memory usage reached 95% threshold on worker node prod-wk-07",
            "timestamp": "2025-01-15T10:15:00Z",
            "service": "monitoring-agent",
            "status": "warning",
        },
        {
            "message": "Payment transaction failed due to timeout with external payment provider",
            "timestamp": "2025-01-15T10:20:00Z",
            "service": "payment-service",
            "status": "error",
        },
    ]

    query = "database connection issues causing failures"

    print("=== Embedding All Messages ===")
    embedded = embed_log_messages(sample_messages)
    print(format_embedding_report(embedded))

    print("\n=== Semantic Search ===")
    print(f"Query: {query}")
    print()

    similar = embed_and_find_similar(sample_messages, query, top_k=3)

    for i, result in enumerate(similar, 1):
        entry = result.get("log_entry", {})
        print(f"[{i}] Similarity: {result['similarity']:.4f}")
        print(f"    Service: {entry.get('service', 'unknown')}")
        print(f"    Message: {entry.get('message', '')}")
        print()

    print("\n--- Raw JSON (first 2 embeddings preview) ---")
    preview = embedded[:2]
    for p in preview:
        p["embedding"] = p["embedding"][:10]  # truncate for readability
    print(json.dumps(preview, indent=2))


if __name__ == "__main__":
    main()
