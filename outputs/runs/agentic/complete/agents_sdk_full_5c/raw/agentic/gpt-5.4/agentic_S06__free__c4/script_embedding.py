from __future__ import annotations

from openai import OpenAI

from speech_models import EmbeddingResult


OPENAI_EMBEDDING_MODEL = "text-embedding-3-large"


def embed_script(text: str) -> EmbeddingResult:
    client = OpenAI()
    response = client.embeddings.create(
        model=OPENAI_EMBEDDING_MODEL,
        input=text,
    )
    return EmbeddingResult(
        vector=list(response.data[0].embedding),
        model=OPENAI_EMBEDDING_MODEL,
    )
