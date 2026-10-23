from __future__ import annotations

from typing import Any

from embeddings_client import DEFAULT_EMBED_MODEL


def summarize_embedding_job(
    results: list[dict[str, Any]], model: str = DEFAULT_EMBED_MODEL
) -> dict[str, Any]:
    completed = sum(1 for item in results if item.get("status") == "embedded")
    failed = sum(1 for item in results if item.get("status") == "failed")
    vector_sizes = [
        int(item.get("dimensions", 0)) for item in results if item.get("dimensions")
    ]
    return {
        "provider": "Cohere",
        "model": model,
        "api_host": "api.cohere.com",
        "total_items": len(results),
        "completed_items": completed,
        "failed_items": failed,
        "average_dimensions": (sum(vector_sizes) / len(vector_sizes))
        if vector_sizes
        else 0,
    }
