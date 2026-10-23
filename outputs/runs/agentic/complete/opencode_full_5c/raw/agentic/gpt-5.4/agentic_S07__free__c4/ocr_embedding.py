from __future__ import annotations

import os
from typing import Sequence

from openai import OpenAI

from document_models import EmbeddingResult


OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-large"


def embed_document_sections(sections: Sequence[str]) -> EmbeddingResult:
    client = OpenAI(api_key=os.environ[OPENAI_API_KEY_ENV])
    response = client.embeddings.create(
        model=OPENAI_EMBEDDING_MODEL, input=list(sections)
    )
    vectors = [item.embedding for item in response.data]
    return EmbeddingResult(
        provider="openai",
        vectors=vectors,
        model=OPENAI_EMBEDDING_MODEL,
        raw_response=response.model_dump() if hasattr(response, "model_dump") else {},
    )
