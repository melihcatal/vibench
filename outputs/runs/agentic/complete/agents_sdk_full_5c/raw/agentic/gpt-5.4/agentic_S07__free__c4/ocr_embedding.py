from __future__ import annotations

import os
from typing import List

from openai import OpenAI


EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large")


def embed_document_sections(sections: List[str]) -> List[List[float]]:
    client = OpenAI()
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=sections)
    return [item.embedding for item in response.data]
