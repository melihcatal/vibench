from __future__ import annotations

import os

from openai import OpenAI


def embed_moderation_rationales(
    rationales: list[str],
    model: str = "text-embedding-3-large",
) -> dict:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.embeddings.create(model=model, input=rationales)
    return {
        "provider": "OpenAI Embeddings",
        "model": model,
        "vectors": [item.embedding for item in response.data],
    }
