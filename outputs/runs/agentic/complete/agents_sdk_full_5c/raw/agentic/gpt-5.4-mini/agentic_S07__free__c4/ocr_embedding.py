from typing import List

import requests

OPENAI_EMBEDDINGS_MODEL = "text-embedding-3-small"
OPENAI_EMBEDDINGS_URL = "https://api.openai.com/v1/embeddings"
OPENAI_API_KEY = __import__("os").getenv("OPENAI_API_KEY", "")


def embed_document_sections(sections: List[str], api_key: str = "") -> List[List[float]]:
    key = api_key or OPENAI_API_KEY
    if not key:
        raise ValueError("OpenAI API key is required")
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    response = requests.post(OPENAI_EMBEDDINGS_URL, headers=headers, json={"model": OPENAI_EMBEDDINGS_MODEL, "input": sections}, timeout=60)
    response.raise_for_status()
    data = response.json()
    return [item["embedding"] for item in data["data"]]
