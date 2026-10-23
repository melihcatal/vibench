import os
from typing import List

import requests


OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
OPENAI_EMBEDDING_API_HOST = "https://api.openai.com/v1/embeddings"


def embed_translated_segments(segments: List[str]) -> List[List[float]]:
    api_key = os.getenv(OPENAI_API_KEY_ENV, "")
    payload = {"model": OPENAI_EMBEDDING_MODEL, "input": segments}
    response = requests.post(OPENAI_EMBEDDING_API_HOST, headers={"Authorization": f"Bearer {api_key}"}, json=payload, timeout=30)
    response.raise_for_status()
    return [item["embedding"] for item in response.json().get("data", [])]
