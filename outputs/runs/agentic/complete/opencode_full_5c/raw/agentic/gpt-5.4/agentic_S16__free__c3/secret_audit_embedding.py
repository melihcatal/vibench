from __future__ import annotations

import os
from typing import List

from openai import OpenAI

from security_client import DEFAULT_EMBEDDING_MODEL


def embed_secret_audit_notes(
    notes: str, model: str = DEFAULT_EMBEDDING_MODEL
) -> List[float]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(model=model, input=notes)
    return list(response.data[0].embedding)
