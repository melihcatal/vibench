from __future__ import annotations

import os
from typing import List

from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def embed_document_sections(sections: List[str]) -> List[List[float]]:
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=sections)
    return [item.embedding for item in response.data]
