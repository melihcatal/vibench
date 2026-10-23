from __future__ import annotations

import os
from typing import Iterable, List, Sequence

from openai import OpenAI


OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def _chunk_texts(texts: Sequence[str], batch_size: int) -> Iterable[Sequence[str]]:
    for start in range(0, len(texts), batch_size):
        yield texts[start : start + batch_size]


def embed_batch(texts: Sequence[str], batch_size: int = 100, model: str = OPENAI_EMBEDDING_MODEL) -> List[List[float]]:
    if batch_size <= 0:
        raise ValueError("batch_size must be positive")
    client = OpenAI()
    embeddings: List[List[float]] = []
    for chunk in _chunk_texts(list(texts), batch_size):
        response = client.embeddings.create(model=model, input=list(chunk))
        embeddings.extend([item.embedding for item in response.data])
    return embeddings


if __name__ == "__main__":
    import json
    import sys

    payload = json.loads(sys.stdin.read() or "[]")
    if not isinstance(payload, list):
        raise TypeError("Expected a JSON array of texts on stdin")
    result = embed_batch([str(item) for item in payload])
    print(json.dumps(result))
