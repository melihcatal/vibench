from __future__ import annotations

import os
from typing import List

from openai import OpenAI

from model_models import EmbeddingRequest

EMBEDDING_MODEL = "text-embedding-3-small"


def embed_output(texts: List[str], model: str | None = None) -> list[list[float]]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    req = EmbeddingRequest(texts=texts, model=model or EMBEDDING_MODEL)
    response = client.embeddings.create(model=req.model, input=req.texts)
    return [item.embedding for item in response.data]
