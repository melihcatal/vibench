import os
from typing import List

from openai import OpenAI


OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def embed_crypto_audit_notes(notes: List[str]) -> List[List[float]]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=notes)
    return [item.embedding for item in response.data]


def embed_single_crypto_audit_note(note: str) -> List[float]:
    return embed_crypto_audit_notes([note])[0]
