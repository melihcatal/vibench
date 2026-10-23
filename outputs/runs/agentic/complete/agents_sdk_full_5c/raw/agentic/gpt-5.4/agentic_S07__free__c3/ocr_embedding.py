from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI

from document_models import EmbeddingResult


def embed_document_sections(sections: Iterable[str]) -> EmbeddingResult:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    inputs: List[str] = list(sections)
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=inputs,
    )
    vectors = [item.embedding for item in response.data]
    return EmbeddingResult(
        provider="openai",
        model="text-embedding-3-large",
        vectors=vectors,
    )
