from __future__ import annotations

from typing import List

from openai import OpenAI

from safety_client import OPENAI_EMBEDDING_MODEL, get_openai_client


def moderation_reason_embedding(reason_text: str) -> List[float]:
    client: OpenAI = get_openai_client()
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=reason_text)
    return list(response.data[0].embedding)
