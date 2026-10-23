from collections import Counter
from typing import Iterable, Mapping

from openai import OpenAI

from embeddings_models import normalize_embedding

OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def embedding_job_summary(job_results: Iterable[Mapping[str, object]]) -> dict[str, object]:
    client = OpenAI()
    embeddings = [normalize_embedding(result["embedding"]) for result in job_results if "embedding" in result]
    model_count = Counter(str(result.get("model", OPENAI_EMBEDDING_MODEL)) for result in job_results)
    return {
        "provider": "openai",
        "model_counts": dict(model_count),
        "num_embeddings": len(embeddings),
        "mean_embedding": [sum(values) / len(values) for values in zip(*embeddings)] if embeddings else [],
        "openai_client_type": type(client).__name__,
    }
