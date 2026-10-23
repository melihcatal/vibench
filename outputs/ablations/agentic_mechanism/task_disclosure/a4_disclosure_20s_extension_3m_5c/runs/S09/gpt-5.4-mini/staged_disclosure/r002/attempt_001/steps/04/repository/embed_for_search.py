import os
from typing import List

import requests


OPENAI_API_URL = "https://api.openai.com/v1/embeddings"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def _embed(inputs: List[str]) -> List[List[float]]:
    api_key = os.environ["OPENAI_API_KEY"]
    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={"model": OPENAI_EMBEDDING_MODEL, "input": inputs},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    return [item["embedding"] for item in sorted(payload["data"], key=lambda x: x["index"])]


def embed_query_and_documents(query: str, documents: List[str]) -> dict:
    vectors = _embed([query, *documents])
    return {"query_embedding": vectors[0], "document_embeddings": vectors[1:]}
