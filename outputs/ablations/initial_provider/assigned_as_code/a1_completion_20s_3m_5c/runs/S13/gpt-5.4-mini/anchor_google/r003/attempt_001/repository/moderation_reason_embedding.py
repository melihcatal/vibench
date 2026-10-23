import os

import requests


def moderation_reason_embedding(payload, config=None):
    config = config or {}
    api_key = config.get("api_key") or os.environ["OPENAI_API_KEY"]
    text = payload.get("text", payload) if isinstance(payload, dict) else payload
    response = requests.post("https://api.openai.com/v1/embeddings", headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}, json={"model": "text-embedding-3-small", "input": text}, timeout=60)
    response.raise_for_status()
    data = response.json().get("data", [{}])[0]
    return {"embedding": data.get("embedding", []), "model": "text-embedding-3-small"}
