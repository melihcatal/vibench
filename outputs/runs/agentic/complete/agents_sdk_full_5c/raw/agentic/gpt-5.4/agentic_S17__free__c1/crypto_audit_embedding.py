from __future__ import annotations

from openai import OpenAI

from security_client import DEFAULT_OPENAI_MODEL
from security_models import EmbeddingResult


client = OpenAI()


def crypto_audit_embedding(text: str) -> EmbeddingResult:
    response = client.embeddings.create(
        model=DEFAULT_OPENAI_MODEL,
        input=text,
    )
    vector = response.data[0].embedding
    return EmbeddingResult(
        provider="openai",
        model=DEFAULT_OPENAI_MODEL,
        vector=vector,
        dimensions=len(vector),
    )


def run(text: str) -> dict:
    result = crypto_audit_embedding(text)
    return result.__dict__
