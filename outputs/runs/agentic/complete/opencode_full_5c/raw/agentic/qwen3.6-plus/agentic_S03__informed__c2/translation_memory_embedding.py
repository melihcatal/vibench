import os
from typing import Optional

import openai


def embed_translation_segments(
    segments: list[str],
    model: str = "text-embedding-3-small",
    dimensions: Optional[int] = None,
) -> list[list[float]]:
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = openai.OpenAI(api_key=api_key)

    params: dict = {
        "model": model,
        "input": segments,
    }
    if dimensions is not None:
        params["dimensions"] = dimensions

    response = client.embeddings.create(**params)

    embeddings = []
    for item in response.data:
        embeddings.append(item.embedding)

    return embeddings


def build_translation_memory_index(
    segments: list[str],
    model: str = "text-embedding-3-small",
    dimensions: Optional[int] = None,
) -> dict:
    embeddings = embed_translation_segments(
        segments, model=model, dimensions=dimensions
    )
    return {
        "segments": segments,
        "embeddings": embeddings,
        "model": model,
        "dimensions": len(embeddings[0]) if embeddings else 0,
        "segment_count": len(segments),
    }


def search_translation_memory(
    query: str,
    index: dict,
    top_k: int = 5,
) -> list[dict]:
    query_embedding = embed_translation_segments([query], model=index["model"])[0]

    scored = []
    for i, segment_embedding in enumerate(index["embeddings"]):
        similarity = cosine_similarity(query_embedding, segment_embedding)
        scored.append(
            {
                "segment": index["segments"][i],
                "similarity": similarity,
                "index": i,
            }
        )

    scored.sort(key=lambda x: x["similarity"], reverse=True)
    return scored[:top_k]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot_product = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)
