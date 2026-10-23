from __future__ import annotations

from openai import OpenAI

from security_models import EmbeddingNote


client = OpenAI()


def crypto_audit_embedding(text: str) -> dict:
    embedding = client.embeddings.create(model="text-embedding-3-small", input=text)
    vector = embedding.data[0].embedding
    note = EmbeddingNote(text=text, vector=vector, provider="openai")
    return note.__dict__
