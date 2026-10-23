from __future__ import annotations

from typing import Iterable, List

from openai import OpenAI

from document_models import EmbeddingResult


EMBEDDING_MODEL = "text-embedding-3-large"


def embed_document_sections(sections: Iterable[str]) -> EmbeddingResult:
    client = OpenAI()
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=list(sections))
    vectors: List[List[float]] = [item.embedding for item in response.data]
    return EmbeddingResult(embeddings=vectors, model=EMBEDDING_MODEL)
