import os
from typing import Iterable, List, Sequence

from openai import OpenAI


DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def _normalize_note(note: str) -> str:
    return " ".join(note.strip().split())


def _prepare_inputs(notes: Sequence[str]) -> List[str]:
    return [_normalize_note(note) for note in notes if note and note.strip()]


def embed_crypto_audit_notes(notes: Sequence[str], model: str = DEFAULT_EMBEDDING_MODEL) -> List[List[float]]:
    prepared = _prepare_inputs(notes)
    if not prepared:
        return []
    client = OpenAI()
    response = client.embeddings.create(model=model, input=prepared)
    return [item.embedding for item in response.data]


def embed_single_crypto_audit_note(note: str, model: str = DEFAULT_EMBEDDING_MODEL) -> List[float]:
    embeddings = embed_crypto_audit_notes([note], model=model)
    return embeddings[0] if embeddings else []


def batch_embed_crypto_audit_notes(notes: Iterable[str], batch_size: int = 64, model: str = DEFAULT_EMBEDDING_MODEL) -> List[List[float]]:
    all_embeddings: List[List[float]] = []
    batch: List[str] = []
    for note in notes:
        if note and note.strip():
            batch.append(note)
        if len(batch) >= batch_size:
            all_embeddings.extend(embed_crypto_audit_notes(batch, model=model))
            batch = []
    if batch:
        all_embeddings.extend(embed_crypto_audit_notes(batch, model=model))
    return all_embeddings
