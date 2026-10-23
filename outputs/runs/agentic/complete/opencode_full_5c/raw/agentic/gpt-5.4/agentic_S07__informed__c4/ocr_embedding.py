from __future__ import annotations

from openai import OpenAI

from document_models import EmbeddingResult


OPENAI_EMBEDDING_MODEL = "text-embedding-3-large"


def embed_ocr_sections(sections: list[str]) -> EmbeddingResult:
    client = OpenAI()
    response = client.embeddings.create(
        model=OPENAI_EMBEDDING_MODEL,
        input=sections,
    )
    embeddings = [item.embedding for item in response.data]
    return EmbeddingResult(
        provider="openai",
        model=OPENAI_EMBEDDING_MODEL,
        embeddings=embeddings,
        raw=response,
    )
