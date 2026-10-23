import os
from typing import Iterable, List, Sequence

import requests


OPENAI_EMBEDDINGS_URL = "https://api.openai.com/v1/embeddings"
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def _normalize_input(text: str) -> str:
    return text if text is not None else ""


def embed_platform_output(text: str, api_key: str | None = None, model: str | None = None) -> List[float]:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required")
    payload = {"input": _normalize_input(text), "model": model or OPENAI_EMBEDDING_MODEL}
    response = requests.post(
        OPENAI_EMBEDDINGS_URL,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["data"][0]["embedding"]


def embed_platform_outputs(texts: Sequence[str], api_key: str | None = None, model: str | None = None) -> List[List[float]]:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required")
    payload = {"input": [_normalize_input(text) for text in texts], "model": model or OPENAI_EMBEDDING_MODEL}
    response = requests.post(
        OPENAI_EMBEDDINGS_URL,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return [item["embedding"] for item in data["data"]]
