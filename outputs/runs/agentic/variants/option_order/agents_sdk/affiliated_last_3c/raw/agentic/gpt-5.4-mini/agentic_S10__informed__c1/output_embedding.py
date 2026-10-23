from __future__ import annotations

import os

from openai import OpenAI

from model_models import EmbeddingResult, normalize_text


def embed_output(text: str) -> EmbeddingResult:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    response = client.embeddings.create(model=model, input=normalize_text(text))
    vector = list(response.data[0].embedding)
    return EmbeddingResult(input_text=text, vector=vector, model=model, raw=response)
