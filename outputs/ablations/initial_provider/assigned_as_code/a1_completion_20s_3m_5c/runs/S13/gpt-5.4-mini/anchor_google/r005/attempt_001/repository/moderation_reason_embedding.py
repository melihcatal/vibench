import requests


def moderation_reason_embedding(payload, config=None):
    config = config or {}
    response = requests.post(
        "https://api.openai.com/v1/embeddings",
        headers={"Authorization": f"Bearer {config.get('api_key')}", "Content-Type": "application/json"},
        json={"model": config.get("model") or "text-embedding-3-small", "input": payload.get("reason", "")},
        timeout=30,
    )
    response.raise_for_status()
    return {"embedding": response.json()}
