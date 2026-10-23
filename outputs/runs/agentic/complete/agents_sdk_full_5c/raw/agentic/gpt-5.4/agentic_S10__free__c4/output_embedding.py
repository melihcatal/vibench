from __future__ import annotations

from openai import OpenAI

from model_client import DEFAULT_EMBEDDING_MODEL
from model_models import EmbeddingResult


def output_embedding(text: str) -> EmbeddingResult:
    client = OpenAI()
    response = client.embeddings.create(
        model=DEFAULT_EMBEDDING_MODEL,
        input=text,
    )
    item = response.data[0]
    return EmbeddingResult(
        vector=item.embedding,
        model=response.model,
        raw=response,
    )
