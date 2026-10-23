import json
from typing import Any, Dict, List


def summarize_embedding_job(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Summarize results of an embedding batch job.

    Args:
        results (List[Dict[str, Any]]): List of individual embedding results.

    Returns:
        Dict[str, Any]: Summary containing counts, sample embeddings, and metadata.
    """
    total = len(results)
    sample = results[:3] if total > 0 else []
    return {
        "total_embeddings": total,
        "sample_embeddings": sample,
        "metadata": {
            "embedding_provider": "openai",  # replace with actual provider
            "created_at": "2025-01-01T00:00:00Z",
        },
    }
