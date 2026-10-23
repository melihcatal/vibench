from __future__ import annotations

from typing import List

from safety_client import openai_get_embedding_model, openai_post


def moderation_reason_embedding(reason: str) -> List[float]:
    payload = {
        "model": openai_get_embedding_model(),
        "input": reason,
    }
    response = openai_post("/v1/embeddings", payload)
    return response["data"][0]["embedding"]
