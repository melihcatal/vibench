import os

import requests


def moderation_reason_embedding(payload, config=None):
    text = payload["text"] if isinstance(payload, dict) else str(payload)
    response = requests.post(
        "https://api.openai.com/v1/embeddings",
        headers={"Authorization": f"Bearer {((config or {}).get('api_key') or os.environ['OPENAI_API_KEY'])}", "Content-Type": "application/json"},
        json={"model": "text-embedding-3-large", "input": text},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
