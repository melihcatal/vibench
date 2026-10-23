from __future__ import annotations

import os
from typing import List

from openai import OpenAI

from document_models import NormalizedDocument

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def embed_document_sections(document: NormalizedDocument) -> List[List[float]]:
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is required")
    client = OpenAI(api_key=OPENAI_API_KEY)
    inputs = [section.get("content", "") for section in document.sections] or [document.text]
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=inputs)
    return [item.embedding for item in response.data]
