"""
Embeds selected log messages for semantic retrieval using OpenAI Embeddings API.
Provider: OpenAI Embeddings (text-embedding-3-small)
Auth: OPENAI_API_KEY
"""

import os
from typing import List, Dict, Any
from openai import OpenAI


EMBEDDING_MODEL_ID = "text-embedding-3-small"


def get_openai_api_key() -> str:
    """Retrieve OpenAI API key from environment."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return api_key


def embed_log_messages(
    messages: List[str],
    model: str = EMBEDDING_MODEL_ID,
) -> List[Dict[str, Any]]:
    """Generate embeddings for a list of log messages using OpenAI embeddings.

    Uses the OpenAI API (api.openai.com) with the text-embedding-3-small model
    to produce vector representations suitable for semantic search.
    """
    api_key = get_openai_api_key()
    client = OpenAI(api_key=api_key)

    non_empty = [(i, msg) for i, msg in enumerate(messages) if msg.strip()]
    if not non_empty:
        return []

    texts = [msg for _, msg in non_empty]
    response = client.embeddings.create(
        model=model,
        input=texts,
    )

    results = []
    for (orig_index, orig_text), emb_data in zip(non_empty, response.data):
        results.append({
            "original_index": orig_index,
            "message": orig_text,
            "embedding": emb_data.embedding,
            "model": model,
            "usage_tokens": response.usage.total_tokens,
        })
    return results


def embed_single_log_message(
    message: str,
    model: str = EMBEDDING_MODEL_ID,
) -> Dict[str, Any]:
    """Embed a single log message and return its vector representation."""
    results = embed_log_messages([message], model=model)
    return results[0] if results else {}


if __name__ == "__main__":
    sample_logs = [
        "Database connection pool exhausted on primary node",
        "User authentication failed with invalid credentials",
        "Memory utilization exceeded 85% on application server",
        "Request timeout after 30s waiting for upstream response",
    ]
    embeddings = embed_log_messages(sample_logs)
    for e in embeddings:
        vec_preview = e["embedding"][:5]
        print(f"[{e['message']}] embedding dim={len(e['embedding'])} preview={vec_preview}")
