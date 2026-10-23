from __future__ import annotations

from typing import List

from safety_client import get_client, get_config


def moderation_reason_embedding(rationale: str) -> List[float]:
    config = get_config()
    client = get_client(config.api_key)
    response = client.embeddings.create(model=config.embedding_model, input=rationale)
    return list(response.data[0].embedding)
