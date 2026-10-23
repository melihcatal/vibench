from __future__ import annotations

import os

from openai import OpenAI

from translation_models import EmbeddingResult


def embed_translation_segment(text: str) -> EmbeddingResult:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )
    vector = list(response.data[0].embedding)
    return EmbeddingResult(embedding=vector, dimensions=len(vector), raw=response)
