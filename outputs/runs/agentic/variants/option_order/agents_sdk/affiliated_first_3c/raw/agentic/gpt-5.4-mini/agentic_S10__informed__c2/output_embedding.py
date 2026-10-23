from __future__ import annotations

from model_client import DEFAULT_EMBEDDING_MODEL, openai_embedding
from model_models import EmbeddingResult


def embed_output(text: str, model: str = DEFAULT_EMBEDDING_MODEL) -> EmbeddingResult:
    vector = openai_embedding(text=text, model=model)
    return EmbeddingResult(vector=vector, model=model)
