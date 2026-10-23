from __future__ import annotations

import os

from openai import OpenAI

from speech_models import EmbeddingResult


def embed_script(text: str, model: str = "text-embedding-3-large") -> EmbeddingResult:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is required")
    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(model=model, input=text)
    vector = response.data[0].embedding
    return EmbeddingResult(
        provider="openai", model=model, embedding=vector, dimensions=len(vector)
    )
