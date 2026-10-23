import os
from typing import List, Sequence

from openai import OpenAI


EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def _client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return OpenAI(api_key=api_key)


def embed_moderation_reasons(reasons: Sequence[str]) -> List[List[float]]:
    texts = [reason.strip() for reason in reasons if reason and reason.strip()]
    if not texts:
        return []
    response = _client().embeddings.create(model=EMBEDDING_MODEL, input=texts)
    vectors = sorted(response.data, key=lambda item: item.index)
    return [item.embedding for item in vectors]


def embed_moderation_reason(reason: str) -> List[float]:
    vectors = embed_moderation_reasons([reason])
    return vectors[0] if vectors else []
