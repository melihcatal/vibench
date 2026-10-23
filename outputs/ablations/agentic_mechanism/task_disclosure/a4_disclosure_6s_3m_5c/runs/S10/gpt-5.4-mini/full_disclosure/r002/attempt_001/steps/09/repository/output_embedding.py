import os
from typing import Iterable, List, Sequence

import requests


OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")


def _normalize_inputs(outputs: Sequence[str] | str) -> List[str]:
    if isinstance(outputs, str):
        return [outputs]
    return [str(item) for item in outputs]


def embed_outputs(outputs: Sequence[str] | str) -> List[List[float]]:
    texts = _normalize_inputs(outputs)
    if not texts:
        return []
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is required for OpenAI embeddings")

    response = requests.post(
        f"{OPENAI_API_BASE.rstrip('/')}/embeddings",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        json={"model": OPENAI_EMBEDDING_MODEL, "input": texts},
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    data = sorted(payload.get("data", []), key=lambda item: item.get("index", 0))
    return [item["embedding"] for item in data]
