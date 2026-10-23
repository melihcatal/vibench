from __future__ import annotations

import os
from typing import Dict, Iterable, List

from openai import OpenAI

OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-large"


def transcript_embedding(segments: Iterable[str]) -> Dict[str, List[List[float]]]:
    api_key = os.getenv(OPENAI_API_KEY_ENV)
    if not api_key:
        raise RuntimeError(f"Missing required environment variable: {OPENAI_API_KEY_ENV}")

    texts = list(segments)
    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=texts)
    return {
        "provider": "OpenAI",
        "model": OPENAI_EMBEDDING_MODEL,
        "embeddings": [item.embedding for item in response.data],
    }
