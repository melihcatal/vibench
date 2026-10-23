from __future__ import annotations

from document_client import get_openai_client
from document_models import EmbeddingResult


def embed_document_sections(
    sections: list[str], model: str = "text-embedding-3-large"
) -> EmbeddingResult:
    client = get_openai_client()
    response = client.embeddings.create(model=model, input=sections)
    embeddings = [item.embedding for item in response.data]
    return EmbeddingResult(
        provider="openai", model=model, embeddings=embeddings, raw=response
    )
