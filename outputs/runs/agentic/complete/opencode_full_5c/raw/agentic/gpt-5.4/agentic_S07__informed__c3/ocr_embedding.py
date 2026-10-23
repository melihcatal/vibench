from __future__ import annotations

import os

from openai import OpenAI


EMBEDDING_MODEL = "text-embedding-3-large"


def embed_document_sections(sections: list[str]) -> dict:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=sections)
    return {
        "provider": "openai",
        "model": EMBEDDING_MODEL,
        "embeddings": [item.embedding for item in response.data],
    }
