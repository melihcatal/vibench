import os
from typing import Iterable, List, Sequence

from openai import OpenAI


DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"


def _chunk_text(text: str, max_chars: int = 4000) -> List[str]:
    text = (text or "").strip()
    if not text:
        return []
    chunks = []
    start = 0
    while start < len(text):
        end = min(len(text), start + max_chars)
        if end < len(text):
            split_at = text.rfind("\n", start, end)
            if split_at > start + max_chars // 4:
                end = split_at
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end
    return chunks


def embed_crypto_audit_notes(notes: Sequence[str], model: str = DEFAULT_EMBEDDING_MODEL) -> List[List[float]]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    clean_notes = []
    for note in notes:
        clean_notes.extend(_chunk_text(note))
    if not clean_notes:
        return []
    response = client.embeddings.create(model=model, input=clean_notes)
    return [item.embedding for item in response.data]


def embed_crypto_audit_note(note: str, model: str = DEFAULT_EMBEDDING_MODEL) -> List[List[float]]:
    return embed_crypto_audit_notes([note], model=model)


def semantic_search_query_embedding(query: str, model: str = DEFAULT_EMBEDDING_MODEL) -> List[float]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(model=model, input=query.strip())
    return response.data[0].embedding
