from __future__ import annotations

import math
from typing import List, Optional

from model_client import create_embedding
from model_models import EmbeddingRequest, EmbeddingResponse


def embed_text(
    text: str,
    model: str = "text-embedding-3-small",
    dimensions: Optional[int] = None,
) -> EmbeddingResponse:
    request = EmbeddingRequest(
        model=model,
        input_text=text,
        dimensions=dimensions,
    )
    return create_embedding(request)


def get_embedding_vector(
    text: str,
    model: str = "text-embedding-3-small",
    dimensions: Optional[int] = None,
) -> List[float]:
    response = embed_text(text, model=model, dimensions=dimensions)
    return response.embedding


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


def embed_texts(
    texts: List[str],
    model: str = "text-embedding-3-small",
    dimensions: Optional[int] = None,
) -> List[List[float]]:
    vectors: List[List[float]] = []
    for text in texts:
        response = embed_text(text, model=model, dimensions=dimensions)
        vectors.append(response.embedding)
    return vectors


def find_most_similar(
    query: str,
    candidates: List[str],
    top_k: int = 5,
    model: str = "text-embedding-3-small",
) -> List[tuple]:
    query_vector = get_embedding_vector(query, model=model)
    candidate_vectors = embed_texts(candidates, model=model)

    similarities = []
    for i, cand_vec in enumerate(candidate_vectors):
        sim = cosine_similarity(query_vector, cand_vec)
        similarities.append((i, candidates[i], sim))

    similarities.sort(key=lambda x: x[2], reverse=True)
    return similarities[:top_k]


if __name__ == "__main__":
    import sys

    input_text = sys.stdin.read()
    response = embed_text(input_text)
    print(f"Model: {response.model}")
    print(f"Dimensions: {len(response.embedding)}")
    print(f"First 5 values: {response.embedding[:5]}")
