import os
from typing import List

import requests

OPENAI_EMBEDDINGS_URL = "https://api.openai.com/v1/embeddings"
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def embed_translation_segments(segments: List[str]) -> List[List[float]]:
    api_key = os.getenv(OPENAI_API_KEY_ENV, "")
    if not api_key:
        raise ValueError(f"Missing {OPENAI_API_KEY_ENV}")
    resp = requests.post(
        OPENAI_EMBEDDINGS_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": OPENAI_EMBEDDING_MODEL, "input": segments},
        timeout=30,
    )
    resp.raise_for_status()
    return [item["embedding"] for item in resp.json()["data"]]
