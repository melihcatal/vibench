import os
from typing import Iterable, List, Sequence

import requests


OPENAI_EMBEDDINGS_URL = "https://api.openai.com/v1/embeddings"
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def _normalize_segments(segments: Iterable[str]) -> List[str]:
    normalized: List[str] = []
    for segment in segments:
        if segment is None:
            continue
        text = str(segment).strip()
        if text:
            normalized.append(text)
    return normalized


def embed_translation_memory_segments(segments: Sequence[str], api_key: str | None = None) -> List[List[float]]:
    cleaned_segments = _normalize_segments(segments)
    if not cleaned_segments:
        return []

    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    response = requests.post(
        OPENAI_EMBEDDINGS_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_EMBEDDING_MODEL,
            "input": cleaned_segments,
        },
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()

    data = payload.get("data", [])
    embeddings: List[List[float]] = []
    for item in data:
        embedding = item.get("embedding")
        if isinstance(embedding, list):
            embeddings.append([float(value) for value in embedding])
    return embeddings


def build_translation_memory_index(segments: Sequence[str], api_key: str | None = None) -> dict:
    cleaned_segments = _normalize_segments(segments)
    embeddings = embed_translation_memory_segments(cleaned_segments, api_key=api_key)
    return {
        "provider": "openai",
        "model": OPENAI_EMBEDDING_MODEL,
        "segments": cleaned_segments,
        "embeddings": embeddings,
    }
