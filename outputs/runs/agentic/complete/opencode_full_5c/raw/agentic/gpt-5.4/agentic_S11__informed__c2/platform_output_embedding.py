from __future__ import annotations

import os
from typing import Any, Dict

from openai import OpenAI


OPENAI_EMBEDDING_MODEL = "text-embedding-3-large"


def embed_platform_output(text: str) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=text)
    item = response.data[0]
    return {
        "provider": "OpenAI",
        "model": OPENAI_EMBEDDING_MODEL,
        "embedding": item.embedding,
        "dimensions": len(item.embedding),
        "raw": response,
    }
