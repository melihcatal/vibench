import os
import requests

OPENAI_EMBEDDING_URL = "https://api.openai.com/v1/embeddings"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


def embed_script(text: str):
    r = requests.post(OPENAI_EMBEDDING_URL, headers={"Authorization": f"Bearer {OPENAI_API_KEY}"}, json={"model": "text-embedding-3-small", "input": text})
    r.raise_for_status()
    return r.json()["data"][0]["embedding"]
