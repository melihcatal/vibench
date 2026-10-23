from __future__ import annotations

from openai import OpenAI

from speech_models import EmbeddingResult


PROVIDER = "openai"
MODEL = "text-embedding-3-large"


def embed_script(text: str) -> EmbeddingResult:
    client = OpenAI()
    response = client.embeddings.create(model=MODEL, input=text)
    vector = response.data[0].embedding
    return EmbeddingResult(
        embedding=vector,
        dimensions=len(vector),
        provider=PROVIDER,
        model=MODEL,
    )
