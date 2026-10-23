from __future__ import annotations

from embeddings_client import embed_batch_request
from embeddings_models import cosine_similarity


def score_text_similarity(text_a: str, text_b: str, model: str = "text-embedding-3-small") -> dict:
    response = embed_batch_request([text_a, text_b], model=model)
    ordered = [item.embedding for item in sorted(response.data, key=lambda item: item.index)]
    if len(ordered) != 2:
        raise RuntimeError("OpenAI embeddings API did not return both embeddings.")
    return {
        "provider": "OpenAI",
        "model": response.model,
        "similarity": cosine_similarity(ordered[0], ordered[1]),
    }
