import requests

from translation_client import load_translation_config


def translation_memory_embedding(payload, config=None):
    cfg = load_translation_config(config)
    response = requests.post(
        "https://api.openai.com/v1/embeddings",
        headers={"Authorization": f"Bearer {cfg.api_key}", "Content-Type": "application/json"},
        json={"model": "text-embedding-3-small", "input": payload["segments"]},
        timeout=30,
    )
    response.raise_for_status()
    return {"embeddings": [item["embedding"] for item in response.json()["data"]]}
