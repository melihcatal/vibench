from __future__ import annotations

import requests

from safety_client import get_openai_base_url, get_openai_headers
from safety_models import EmbeddingResult


EMBEDDING_MODEL = "text-embedding-3-large"


def moderation_reason_embedding(reason_text: str) -> EmbeddingResult:
    response = requests.post(
        f"{get_openai_base_url()}/embeddings",
        headers=get_openai_headers(),
        json={"model": EMBEDDING_MODEL, "input": reason_text},
        timeout=30,
    )
    response.raise_for_status()
    body = response.json()
    vector = body["data"][0]["embedding"]
    return EmbeddingResult(vector=vector, dimensions=len(vector), provider="OpenAI")
