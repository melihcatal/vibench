from __future__ import annotations

from typing import List

from openai import OpenAI

from model_models import EmbeddingResult


def platform_output_embedding(text: str, model: str = "text-embedding-3-small") -> EmbeddingResult:
    client = OpenAI()
    response = client.embeddings.create(model=model, input=text)
    vector: List[float] = response.data[0].embedding
    return EmbeddingResult(vector=vector, model_id=model, raw=response)
