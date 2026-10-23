from __future__ import annotations

import os
from typing import Any, Dict, List

from openai import OpenAI

from security_models import normalize_text

EMBED_MODEL = "text-embedding-3-small"


def crypto_audit_embedding(note: Any, api_key: str | None = None) -> Dict[str, Any]:
    client = OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))
    text = normalize_text(note)
    response = client.embeddings.create(model=EMBED_MODEL, input=text)
    embedding = response.data[0].embedding
    return {"model": EMBED_MODEL, "text": text, "embedding": embedding}
