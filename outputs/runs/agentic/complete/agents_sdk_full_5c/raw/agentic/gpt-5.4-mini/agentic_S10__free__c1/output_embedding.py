from __future__ import annotations

from typing import List

from model_client import get_embedding_model_name, get_openai_client

PROVIDER = "openai"
MODEL_FAMILY = "text-embedding-3-small"


def output_embedding(text: str, model: str | None = None) -> List[float]:
    client = get_openai_client()
    response = client.embeddings.create(model=get_embedding_model_name(model), input=text)
    return response.data[0].embedding
