from __future__ import annotations

import os

from openai import OpenAI

from speech_models import EmbeddingResult, first_text


def embed_script(script: str, model: str = "text-embedding-3-large") -> EmbeddingResult:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(model=model, input=first_text(script))
    embedding = response.data[0].embedding
    return EmbeddingResult(embedding=embedding, dimensions=len(embedding), model=model)
