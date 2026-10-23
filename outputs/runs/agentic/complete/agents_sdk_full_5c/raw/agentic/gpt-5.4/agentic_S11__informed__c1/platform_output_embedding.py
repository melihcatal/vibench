from __future__ import annotations

import os
from typing import Any

from openai import OpenAI


DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def platform_output_embedding(text: str) -> dict[str, Any]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.embeddings.create(
        model=DEFAULT_EMBEDDING_MODEL,
        input=text,
    )
    item = response.data[0]
    return {
        "embedding": item.embedding,
        "model": response.model,
        "provider_response": response,
    }
