import os
from typing import List, Dict, Any

import requests


OPENAI_EMBEDDINGS_URL = "https://api.openai.com/v1/embeddings"
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def _embed_texts(texts: List[str]) -> List[List[float]]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")

    response = requests.post(
        OPENAI_EMBEDDINGS_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={"model": OPENAI_EMBEDDING_MODEL, "input": texts},
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()["data"]
    return [item["embedding"] for item in sorted(data, key=lambda x: x["index"])]


def embed_for_search(query: str, documents: List[str]) -> Dict[str, Any]:
    embeddings = _embed_texts([query] + documents)
    return {"query_embedding": embeddings[0], "document_embeddings": embeddings[1:]}
