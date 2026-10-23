import os
import json
import requests
from typing import List, Dict

# Load credentials from env vars
OPENAI_EMBED_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_EMBED_API_KEY:
    raise RuntimeError("Set OPENAI_API_KEY environment variable")

BASE_URL = "https://api.openai.com/v1/embeddings"


def embed_text(prompt: str) -> List[float]:
    """Send a plain-text prompt to OpenAI Embeddings endpoint and return vector list."""
    headers = {
        "Authorization": f"Bearer {OPENAI_EMBED_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {"model": "text-embedding-ada-002", "input": prompt}
    resp = requests.post(BASE_URL, headers=headers, json=payload)
    resp.raise_for_status()
    data = resp.json()
    return data["data"][0]["embedding"]


def embed_texts(texts: List[str]) -> List[List[float]]:
    """Batch version that returns list of vectors (one per text)."""
    headers = {
        "Authorization": f"Bearer {OPENAI_EMBED_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {"model": "text-embedding-ada-002", "input": texts}
    resp = requests.post(BASE_URL, headers=headers, json=payload)
    resp.raise_for_status()
    return [item["embedding"] for item in data["data"]]
