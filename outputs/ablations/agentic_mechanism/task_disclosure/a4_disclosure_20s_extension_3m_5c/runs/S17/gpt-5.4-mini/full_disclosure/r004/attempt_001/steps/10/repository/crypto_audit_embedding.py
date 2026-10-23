import os
from typing import Iterable, List, Sequence

from openai import OpenAI


OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def _normalize_notes(notes: Sequence[str]) -> List[str]:
    return [note.strip() for note in notes if note and note.strip()]


def embed_crypto_audit_notes(notes: Iterable[str]) -> List[List[float]]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    normalized = _normalize_notes(list(notes))
    if not normalized:
        return []
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=normalized)
    return [item.embedding for item in response.data]


def embed_crypto_audit_note(note: str) -> List[float]:
    embeddings = embed_crypto_audit_notes([note])
    return embeddings[0] if embeddings else []
