from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI


EMBEDDING_MODEL = "text-embedding-3-large"


def embed_document_sections(sections: Iterable[str]) -> dict:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    inputs: List[str] = list(sections)
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=inputs)
    vectors = [item.embedding for item in response.data]
    return {
        "provider": "openai",
        "model": EMBEDDING_MODEL,
        "embeddings": vectors,
        "dimensions": len(vectors[0]) if vectors else 0,
    }
