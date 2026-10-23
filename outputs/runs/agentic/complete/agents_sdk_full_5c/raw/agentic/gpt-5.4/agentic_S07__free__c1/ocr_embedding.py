from __future__ import annotations

from document_client import DEFAULT_EMBEDDING_MODEL, get_openai_client, normalize_sections
from document_models import EmbeddingResult


def embed_document_sections(sections: list[str], model: str = DEFAULT_EMBEDDING_MODEL) -> EmbeddingResult:
    client = get_openai_client()
    clean_sections = normalize_sections(sections)
    response = client.embeddings.create(model=model, input=clean_sections)
    vectors = [item.embedding for item in response.data]
    return EmbeddingResult(
        provider="openai",
        model=model,
        embeddings=vectors,
        raw=response.model_dump() if hasattr(response, "model_dump") else None,
    )
