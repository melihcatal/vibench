from __future__ import annotations

import os
from typing import Any

from openai import OpenAI


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
EMBEDDING_MODEL = os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def embed_platform_output(text: str) -> dict[str, Any]:
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    embedding = response.data[0].embedding
    return {"embedding": embedding, "model": response.model, "usage": getattr(response, "usage", None), "raw": response}
