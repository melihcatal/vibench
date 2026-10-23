from __future__ import annotations

import os
from typing import List

from openai import OpenAI

PROVIDER = "OpenAI Embeddings"
EMBEDDING_MODEL = "text-embedding-3-small"


def embed_document_sections(sections: List[str]) -> list[list[float]]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=sections)
    return [item.embedding for item in response.data]
