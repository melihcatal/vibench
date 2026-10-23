from __future__ import annotations

import os
from typing import Sequence

from openai import OpenAI

from security_models import AuditEmbedding

OPENAI_EMBED_MODEL = "text-embedding-3-small"


def embed_secret_audit_notes(notes: str | Sequence[str]) -> AuditEmbedding:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    text = notes if isinstance(notes, str) else "\n".join(notes)
    result = client.embeddings.create(model=OPENAI_EMBED_MODEL, input=text)
    vector = list(result.data[0].embedding)
    return AuditEmbedding(note=text, vector=vector, model=OPENAI_EMBED_MODEL)
