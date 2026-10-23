from __future__ import annotations

import os

from openai import OpenAI

from document_models import normalize_document_text


EMBEDDING_MODEL = "text-embedding-3-large"


def embed_document_sections(text: str) -> dict:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    normalized = normalize_document_text(text)
    inputs = normalized.sections or [normalized.text]
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=inputs)
    vectors = [item.embedding for item in response.data]
    return {
        "provider": "OpenAI",
        "model": EMBEDDING_MODEL,
        "sections": inputs,
        "embeddings": vectors,
    }
