from __future__ import annotations

from openai import OpenAI


def embed_log_messages(
    messages: list[str], model: str = "text-embedding-3-small"
) -> dict:
    client = OpenAI()
    response = client.embeddings.create(model=model, input=messages)
    return {
        "provider": "OpenAI",
        "model": model,
        "embeddings": [item.embedding for item in response.data],
        "dimensions": len(response.data[0].embedding) if response.data else 0,
    }
