from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from typing import Iterable, List, Sequence

import requests


OPENAI_EMBEDDINGS_URL = "https://api.openai.com/v1/embeddings"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


@dataclass(frozen=True)
class EmbeddedSegment:
    segment: str
    embedding: List[float]
    segment_id: str


def _segment_id(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _chunked(items: Sequence[str], size: int) -> Iterable[Sequence[str]]:
    for index in range(0, len(items), size):
        yield items[index : index + size]


def embed_translated_segments(segments: Sequence[str], *, api_key: str | None = None) -> List[EmbeddedSegment]:
    if not segments:
        return []

    token = api_key or os.getenv("OPENAI_API_KEY")
    if not token:
        raise ValueError("OPENAI_API_KEY is required")

    results: List[EmbeddedSegment] = []
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    for batch in _chunked(list(segments), 100):
        response = requests.post(
            OPENAI_EMBEDDINGS_URL,
            headers=headers,
            json={"model": OPENAI_EMBEDDING_MODEL, "input": list(batch)},
            timeout=60,
        )
        response.raise_for_status()
        payload = response.json()
        data = sorted(payload.get("data", []), key=lambda item: item["index"])
        for segment, item in zip(batch, data):
            results.append(
                EmbeddedSegment(
                    segment=segment,
                    embedding=list(item["embedding"]),
                    segment_id=_segment_id(segment),
                )
            )

    return results
