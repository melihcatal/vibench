from __future__ import annotations

from openai import OpenAI

from model_models import EmbeddingRequest

PROVIDER = "openai"
EMBEDDING_MODEL = "text-embedding-3-small"


def embed_outputs(texts: list[str], model: str | None = None) -> list[list[float]]:
    req = EmbeddingRequest(texts=texts, model=model)
    client = OpenAI(api_key=None)
    response = client.embeddings.create(model=req.model or EMBEDDING_MODEL, input=req.texts)
    return [item.embedding for item in response.data]
