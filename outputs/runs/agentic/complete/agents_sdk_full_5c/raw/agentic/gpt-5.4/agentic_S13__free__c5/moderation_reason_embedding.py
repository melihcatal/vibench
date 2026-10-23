from __future__ import annotations

from typing import List

from safety_client import OPENAI_EMBEDDING_MODEL, get_openai_client


def embed_moderation_rationale(rationale: str) -> List[float]:
    client = get_openai_client()
    response = client.embeddings.create(
        model=OPENAI_EMBEDDING_MODEL,
        input=rationale,
    )
    return list(response.data[0].embedding)
