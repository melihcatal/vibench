import os
from typing import Iterable, List

import requests


OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
OPENAI_API_URL = "https://api.openai.com/v1/embeddings"


def _embed(texts: Iterable[str]) -> List[List[float]]:
    api_key = os.environ["OPENAI_API_KEY"]
    payload = {"model": OPENAI_EMBEDDING_MODEL, "input": list(texts)}
    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return [item["embedding"] for item in data["data"]]


def embed_query(query: str) -> List[float]:
    return _embed([query])[0]


def embed_documents(documents: Iterable[str]) -> List[List[float]]:
    return _embed(documents)
