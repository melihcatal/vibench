from __future__ import annotations

from typing import List

from openai import OpenAI

from model_client import choose_model, get_openai_client


def embed_output(text: str, model: str | None = None) -> List[float]:
    client: OpenAI = get_openai_client()
    response = client.embeddings.create(
        model=choose_model(model, family="embedding"),
        input=text,
    )
    return list(response.data[0].embedding)
