from __future__ import annotations

import os

from openai import OpenAI

from speech_models import EmbeddingResult, ensure_text


def embed_script(text: str, model: str = "text-embedding-3-small") -> EmbeddingResult:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(model=model, input=ensure_text(text))
    vector = [float(value) for value in response.data[0].embedding]
    return EmbeddingResult(vector=vector, model=model)
