from __future__ import annotations

from openai import OpenAI

from safety_client import embedding_model, get_openai_api_key


def moderation_reason_embedding(reason_text: str, api_key: str | None = None, model: str | None = None) -> list[float]:
    client = OpenAI(api_key=get_openai_api_key(api_key))
    resolved_model = embedding_model(model)
    response = client.embeddings.create(
        model=resolved_model,
        input=reason_text,
    )
    return response.data[0].embedding
