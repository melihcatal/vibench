import os
from typing import Iterable, List

from openai import OpenAI


OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def _normalize_notes(notes: Iterable[str]) -> List[str]:
    return [note.strip() for note in notes if note and note.strip()]


def embed_secret_audit_notes(notes: Iterable[str]) -> List[List[float]]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    normalized_notes = _normalize_notes(notes)
    if not normalized_notes:
        return []
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=normalized_notes)
    return [item.embedding for item in response.data]


def embed_single_secret_audit_note(note: str) -> List[float]:
    embeddings = embed_secret_audit_notes([note])
    return embeddings[0] if embeddings else []
