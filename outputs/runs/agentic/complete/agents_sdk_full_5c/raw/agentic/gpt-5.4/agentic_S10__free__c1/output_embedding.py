from __future__ import annotations

from model_client import DEFAULT_EMBED_MODEL, get_openai_client
from model_models import EmbeddingResult


def embed_output(text: str) -> EmbeddingResult:
    client = get_openai_client()
    response = client.embeddings.create(
        model=DEFAULT_EMBED_MODEL,
        input=text,
    )
    item = response.data[0]
    return EmbeddingResult(
        vector=item.embedding,
        model=response.model,
        raw_response=response.model_dump(),
    )
