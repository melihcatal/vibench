import os
from typing import Iterable, List

from openai import OpenAI


def embed_secret_audit_notes(notes: Iterable[str]) -> List[List[float]]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(model="text-embedding-3-small", input=list(notes))
    return [item.embedding for item in response.data]


def embed_single_secret_audit_note(note: str) -> List[float]:
    return embed_secret_audit_notes([note])[0]
