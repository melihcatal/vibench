from __future__ import annotations

import os
from typing import List

from openai import OpenAI

from security_models import AuditNote

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def crypto_audit_embedding(note: str) -> List[float]:
    client = OpenAI(api_key=OPENAI_API_KEY)
    audit_note = AuditNote(text=note, labels=["crypto", "audit"], metadata={"provider": "openai"})
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=audit_note.text)
    return list(response.data[0].embedding)
