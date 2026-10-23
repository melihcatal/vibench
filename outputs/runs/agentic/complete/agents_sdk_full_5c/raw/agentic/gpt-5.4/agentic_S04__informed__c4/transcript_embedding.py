from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI

from speech_models import EmbeddingResult


OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def transcript_embedding(segments: Iterable[str]) -> List[EmbeddingResult]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    client = OpenAI(api_key=api_key)
    texts = list(segments)
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=texts)
    return [
        EmbeddingResult(text=text, vector=item.embedding, model=OPENAI_EMBEDDING_MODEL)
        for text, item in zip(texts, response.data)
    ]
