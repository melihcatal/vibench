from __future__ import annotations

import os
from typing import List

from openai import OpenAI

from document_models import chunk_sections


OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def embed_document_sections(text: str) -> List[List[float]]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Missing required environment variable: OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    sections = chunk_sections(text)
    if not sections:
        return []
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=sections)
    return [item.embedding for item in response.data]
