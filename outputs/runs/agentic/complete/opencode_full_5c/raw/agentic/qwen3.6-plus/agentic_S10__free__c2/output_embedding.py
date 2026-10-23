from __future__ import annotations

import math
from typing import Optional

from model_client import create_embedding
from model_models import EmbeddingResponse, normalize_prompt

EMBEDDING_MODEL = "text-embedding-3-small"


def embed_output(
    text: str,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> EmbeddingResponse:
    normalized = normalize_prompt(text)
    return create_embedding(
        text=normalized,
        model=model or EMBEDDING_MODEL,
        api_key=api_key,
        base_url=base_url,
    )


def embed_outputs_batch(
    texts: list[str],
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> list[EmbeddingResponse]:
    results = []
    for text in texts:
        result = embed_output(
            text=text,
            model=model,
            api_key=api_key,
            base_url=base_url,
        )
        results.append(result)
    return results


def cosine_similarity(a: list[float], b: list[float]) -> float:
    if len(a) != len(b):
        raise ValueError("Embedding vectors must have the same dimension")
    dot_product = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


def similarity_between_texts(
    text_a: str,
    text_b: str,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> float:
    emb_a = embed_output(text_a, model=model, api_key=api_key, base_url=base_url)
    emb_b = embed_output(text_b, model=model, api_key=api_key, base_url=base_url)
    return cosine_similarity(emb_a.embedding, emb_b.embedding)


def find_most_similar(
    query: str,
    candidates: list[str],
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> list[tuple[int, float]]:
    query_emb = embed_output(query, model=model, api_key=api_key, base_url=base_url)
    scored = []
    for i, candidate in enumerate(candidates):
        cand_emb = embed_output(
            candidate, model=model, api_key=api_key, base_url=base_url
        )
        score = cosine_similarity(query_emb.embedding, cand_emb.embedding)
        scored.append((i, score))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored


if __name__ == "__main__":
    import os

    response = embed_output(
        text="Machine learning is a subset of artificial intelligence.",
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    print(f"Embedding dimension: {len(response.embedding)}")
    print(f"Model used: {response.model_used}")
