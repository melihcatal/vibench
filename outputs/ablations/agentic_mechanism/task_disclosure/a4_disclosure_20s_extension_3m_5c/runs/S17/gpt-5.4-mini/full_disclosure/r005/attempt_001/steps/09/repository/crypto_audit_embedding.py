import os
from typing import Iterable, List, Sequence

from openai import OpenAI

DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"


def _coerce_notes(notes: Iterable[str]) -> List[str]:
    return [str(note) for note in notes if str(note).strip()]


def embed_crypto_audit_notes(notes: Sequence[str], model: str = DEFAULT_EMBEDDING_MODEL) -> List[List[float]]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    cleaned = _coerce_notes(notes)
    if not cleaned:
        return []
    response = client.embeddings.create(model=model, input=cleaned)
    return [item.embedding for item in response.data]
