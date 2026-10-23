from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI

from security_models import EmbeddingResult


OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def embed_secret_audit_notes(notes: Iterable[str]) -> List[EmbeddingResult]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    note_list = list(notes)
    if not note_list:
        return []
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=note_list)
    return [
        EmbeddingResult(
            model=OPENAI_EMBEDDING_MODEL,
            vector=item.embedding,
            dimensions=len(item.embedding),
        )
        for item in response.data
    ]
