from __future__ import annotations

import os

from openai import OpenAI

from speech_models import EmbeddingResult


EMBEDDING_MODEL = "text-embedding-3-small"


def embed_script(text: str) -> EmbeddingResult:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    item = response.data[0]
    vector = list(item.embedding)
    return EmbeddingResult(
        provider="openai",
        model=EMBEDDING_MODEL,
        embedding=vector,
        dimensions=len(vector),
        raw=response.model_dump(),
    )
