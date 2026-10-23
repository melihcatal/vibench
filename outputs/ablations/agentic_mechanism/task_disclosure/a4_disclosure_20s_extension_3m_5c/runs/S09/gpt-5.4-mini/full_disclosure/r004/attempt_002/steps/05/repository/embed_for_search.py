import os
from typing import List, Dict, Any

import requests


OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")


def _embed(texts: List[str]) -> List[List[float]]:
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is required")
    response = requests.post(
        f"{OPENAI_API_BASE}/embeddings",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        json={"model": OPENAI_EMBEDDING_MODEL, "input": texts},
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    data = sorted(payload["data"], key=lambda item: item["index"])
    return [item["embedding"] for item in data]


def embed_for_search(query: str, documents: List[str]) -> Dict[str, Any]:
    vectors = _embed([query] + documents)
    return {"query_embedding": vectors[0], "document_embeddings": vectors[1:]}
