from __future__ import annotations

import os

from openai import OpenAI

from translation_models import TranslationMemoryEmbeddingResult

OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def embed_translation_segment(segment: str) -> TranslationMemoryEmbeddingResult:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=segment)
    embedding = list(response.data[0].embedding)
    return TranslationMemoryEmbeddingResult(segment=segment, embedding=embedding, model=OPENAI_EMBEDDING_MODEL)
