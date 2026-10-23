from __future__ import annotations

import requests

from translation_client import OPENAI_EMBEDDINGS_ENDPOINT, openai_headers
from translation_models import EmbeddingResult


def translation_memory_embedding(text: str) -> EmbeddingResult:
    model = "text-embedding-3-large"
    response = requests.post(
        OPENAI_EMBEDDINGS_ENDPOINT,
        headers=openai_headers(),
        json={"model": model, "input": text},
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()["data"][0]
    return EmbeddingResult(vector=payload["embedding"], model=model, provider="openai")
