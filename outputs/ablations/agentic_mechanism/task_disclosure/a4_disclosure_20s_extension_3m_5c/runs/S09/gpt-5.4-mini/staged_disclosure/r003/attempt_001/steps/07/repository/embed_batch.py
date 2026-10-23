import json
import os
import sys
from typing import List

import requests


OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")


def embed_batch(texts: List[str]) -> List[List[float]]:
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is required")
    response = requests.post(
        f"{OPENAI_API_BASE.rstrip('/')}/embeddings",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        json={"model": OPENAI_EMBEDDING_MODEL, "input": texts},
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    return [item["embedding"] for item in sorted(payload["data"], key=lambda x: x["index"])]


def main() -> None:
    raw = sys.stdin.read().strip()
    texts = json.loads(raw) if raw else []
    if not isinstance(texts, list) or not all(isinstance(t, str) for t in texts):
        raise ValueError("Expected a JSON array of strings on stdin")
    embeddings = embed_batch(texts)
    json.dump(embeddings, sys.stdout)


if __name__ == "__main__":
    main()
