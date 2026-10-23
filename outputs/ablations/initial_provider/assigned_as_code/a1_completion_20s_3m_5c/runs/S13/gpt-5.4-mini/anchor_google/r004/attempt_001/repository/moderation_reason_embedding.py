import os

import requests

from safety_models import normalize_text


def moderation_reason_embedding(payload, config=None):
    config = config or {}
    api_key = config.get("api_key") or os.environ["OPENAI_API_KEY"]
    text = normalize_text(payload.get("reason"))
    response = requests.post(
        "https://api.openai.com/v1/embeddings",
        headers={"Authorization": f"Bearer {api_key}"},
        json={"model": config.get("model", "text-embedding-3-large"), "input": text},
        timeout=config.get("timeout", 30),
    )
    response.raise_for_status()
    return response.json()
