from __future__ import annotations

from typing import List

from observability_client import load_config


def log_embedding(messages: List[str]) -> List[List[float]]:
    import requests

    cfg = load_config()
    headers = {"Authorization": f"Bearer {cfg.api_key}", "Content-Type": "application/json"}
    payload = {"model": "text-embedding-3-small", "input": messages}
    resp = requests.post("https://api.openai.com/v1/embeddings", json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    return [item["embedding"] for item in resp.json()["data"]]
