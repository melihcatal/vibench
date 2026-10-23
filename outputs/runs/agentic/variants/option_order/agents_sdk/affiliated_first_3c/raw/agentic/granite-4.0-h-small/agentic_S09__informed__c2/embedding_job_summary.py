import json
from embeddings_client import get_embedder

def embedding_job_summary(results: list[dict]) -> dict:
    """Summarize the results of an embedding job."""
    total = len(results)
    if total == 0:
        return {"total": 0, "summary": "No embeddings produced"}
    first = results[0]
    return {
        "total": total,
        "provider": get_embedder().__class__.__name__,
        "example_shape": len(first.get('embeddings', [])),
        "summary": "Embedding job summary"
    }
