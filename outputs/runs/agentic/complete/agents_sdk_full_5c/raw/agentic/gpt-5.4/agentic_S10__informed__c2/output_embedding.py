from __future__ import annotations

import os

from openai import OpenAI

from model_models import EmbeddingResult

DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def embed_output(text: str, *, model: str = DEFAULT_EMBEDDING_MODEL) -> EmbeddingResult:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(model=model, input=text)
    item = response.data[0]
    return EmbeddingResult(vector=item.embedding, model=model, raw=response)
