import os

import requests


def translation_memory_embedding(payload, config=None):
    config = config or {}
    api_key = config.get("api_key") or os.environ.get("OPENAI_API_KEY", "")
    response = requests.post(
        "https://api.openai.com/v1/embeddings",
        headers={"Authorization": f"Bearer {api_key}"},
        json={"model": "text-embedding-3-small", "input": payload["text"]},
        timeout=30,
    )
    response.raise_for_status()
    return {"embedding": response.json()["data"][0]["embedding"]}
