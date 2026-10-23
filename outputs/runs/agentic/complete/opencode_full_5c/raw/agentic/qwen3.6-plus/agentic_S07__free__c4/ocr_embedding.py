import os
from typing import Optional

import requests


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_EMBEDDINGS_API_URL = "https://api.openai.com/v1/embeddings"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-large"


def embed_document_section(
    text: str,
    model: str = OPENAI_EMBEDDING_MODEL,
    dimensions: Optional[int] = None,
) -> dict:
    if not text.strip():
        return {
            "embedding": [],
            "model": model,
            "usage": {"prompt_tokens": 0, "total_tokens": 0},
        }
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "input": text,
        "model": model,
    }
    if dimensions:
        payload["dimensions"] = dimensions
    response = requests.post(
        OPENAI_EMBEDDINGS_API_URL,
        headers=headers,
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    embedding_data = data.get("data", [])
    if not embedding_data:
        return {
            "embedding": [],
            "model": model,
            "usage": data.get("usage", {}),
        }
    return {
        "embedding": embedding_data[0].get("embedding", []),
        "model": model,
        "usage": data.get("usage", {}),
    }


def embed_document_sections(
    texts: list,
    model: str = OPENAI_EMBEDDING_MODEL,
    dimensions: Optional[int] = None,
) -> list:
    if not texts:
        return []
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "input": texts,
        "model": model,
    }
    if dimensions:
        payload["dimensions"] = dimensions
    response = requests.post(
        OPENAI_EMBEDDINGS_API_URL,
        headers=headers,
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    embedding_data = data.get("data", [])
    results = []
    for idx, emb in enumerate(embedding_data):
        results.append(
            {
                "index": emb.get("index", idx),
                "text": texts[idx] if idx < len(texts) else "",
                "embedding": emb.get("embedding", []),
                "model": model,
            }
        )
    return results


def compute_cosine_similarity(embedding_a: list, embedding_b: list) -> float:
    if not embedding_a or not embedding_b:
        return 0.0
    if len(embedding_a) != len(embedding_b):
        raise ValueError("Embeddings must have the same dimension")
    dot_product = sum(a * b for a, b in zip(embedding_a, embedding_b))
    magnitude_a = sum(a * a for a in embedding_a) ** 0.5
    magnitude_b = sum(b * b for b in embedding_b) ** 0.5
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
    return dot_product / (magnitude_a * magnitude_b)


def find_most_similar_section(
    query_embedding: list,
    section_embeddings: list,
    top_k: int = 1,
) -> list:
    similarities = []
    for section in section_embeddings:
        emb = section.get("embedding", [])
        if emb:
            sim = compute_cosine_similarity(query_embedding, emb)
            similarities.append(
                {
                    "index": section.get("index", 0),
                    "text": section.get("text", ""),
                    "similarity": sim,
                }
            )
    similarities.sort(key=lambda x: x["similarity"], reverse=True)
    return similarities[:top_k]
