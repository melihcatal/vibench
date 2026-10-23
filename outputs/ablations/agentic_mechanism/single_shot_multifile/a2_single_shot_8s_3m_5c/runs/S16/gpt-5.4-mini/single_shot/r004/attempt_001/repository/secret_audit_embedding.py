from dataclasses import dataclass
from typing import List

from openai import OpenAI

EMBEDDING_MODEL = "text-embedding-3-small"


@dataclass(frozen=True)
class AuditEmbedding:
    text: str
    vector: List[float]
    model: str


def embed_secret_audit_notes(notes: str) -> AuditEmbedding:
    client = OpenAI()
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=notes)
    vector = response.data[0].embedding
    return AuditEmbedding(text=notes, vector=vector, model=EMBEDDING_MODEL)
