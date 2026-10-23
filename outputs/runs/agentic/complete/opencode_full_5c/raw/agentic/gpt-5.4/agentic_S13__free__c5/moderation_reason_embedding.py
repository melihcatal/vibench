from __future__ import annotations

from openai import OpenAI

from safety_client import openai_config


def moderation_reason_embedding(reason_text: str) -> list[float]:
    config = openai_config()
    client = OpenAI(api_key=config["api_key"])
    response = client.embeddings.create(
        model=config["embedding_model"], input=reason_text
    )
    return list(response.data[0].embedding)
