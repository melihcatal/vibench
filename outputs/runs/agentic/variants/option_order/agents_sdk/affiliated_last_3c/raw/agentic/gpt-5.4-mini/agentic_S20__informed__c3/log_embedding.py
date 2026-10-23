from __future__ import annotations

from openai import OpenAI

from observability_models import EmbeddingResult


client = OpenAI()


def log_embedding(text: str, model: str = "text-embedding-3-small") -> EmbeddingResult:
    response = client.embeddings.create(model=model, input=text)
    vector = response.data[0].embedding if response.data else []
    return EmbeddingResult(text=text, vector=vector, raw=response)
