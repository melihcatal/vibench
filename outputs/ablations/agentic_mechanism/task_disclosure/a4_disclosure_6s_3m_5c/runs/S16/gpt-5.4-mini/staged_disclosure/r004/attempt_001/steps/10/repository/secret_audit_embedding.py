import os
from typing import List, Sequence

from openai import OpenAI


OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def embed_secret_audit_notes(notes: Sequence[str]) -> List[List[float]]:
    if not notes:
        return []
    response = _client().embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=list(notes))
    return [item.embedding for item in response.data]


def embed_single_note(note: str) -> List[float]:
    return embed_secret_audit_notes([note])[0]
