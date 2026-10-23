from __future__ import annotations

import os

from openai import OpenAI

from translation_models import EmbeddingResult


OPENAI_EMBEDDING_PROVIDER = "OpenAI"
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def embed_translated_segment(text: str) -> EmbeddingResult:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.embeddings.create(
        model=OPENAI_EMBEDDING_MODEL,
        input=text,
    )
    vector = list(response.data[0].embedding)
    return EmbeddingResult(
        embedding=vector,
        dimensions=len(vector),
        provider=OPENAI_EMBEDDING_PROVIDER,
        model=OPENAI_EMBEDDING_MODEL,
        raw_response=response,
    )
