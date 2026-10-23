from __future__ import annotations

import os

from openai import OpenAI

from speech_models import EmbeddingResult


OPENAI_EMBEDDING_MODEL = "text-embedding-3-large"


def embed_script(text: str) -> EmbeddingResult:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=text)
    embedding = response.data[0].embedding
    return EmbeddingResult(
        embedding=embedding,
        dimensions=len(embedding),
        raw_response=response.model_dump(),
    )
