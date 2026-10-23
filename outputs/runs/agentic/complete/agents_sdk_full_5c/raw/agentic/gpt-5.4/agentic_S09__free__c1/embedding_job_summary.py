from __future__ import annotations

from collections import Counter
from typing import Any

from embeddings_models import mean_pool


def summarize_embedding_job(job_records: list[dict[str, Any]]) -> dict[str, Any]:
    vectors = [record["embedding"] for record in job_records if record.get("embedding")]
    models = Counter(record.get("model", "text-embedding-3-small") for record in job_records)
    usage_tokens = sum(int(record.get("usage", {}).get("total_tokens", 0)) for record in job_records)
    return {
        "provider": "OpenAI",
        "model_family": "text-embedding-3-small",
        "job_count": len(job_records),
        "successful_embeddings": len(vectors),
        "models": dict(models),
        "total_tokens": usage_tokens,
        "centroid": mean_pool(vectors),
    }
