from __future__ import annotations

from typing import Dict, List

from openai import OpenAI

from safety_client import openai_api_key


def moderation_reason_embedding(reason_text: str) -> Dict[str, List[float] | str]:
    client = OpenAI(api_key=openai_api_key())
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=reason_text,
    )
    return {
        "embedding": response.data[0].embedding,
        "model": "text-embedding-3-large",
        "provider": "openai",
    }
