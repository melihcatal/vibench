import requests

from security_models import normalize_text


def crypto_audit_embedding(payload, config=None):
    config = config or {}
    text = normalize_text(payload.get('notes'))
    response = requests.post(
        "https://api.openai.com/v1/embeddings",
        headers={"Authorization": f"Bearer {config['api_key']}"},
        json={"model": "text-embedding-3-small", "input": text},
        timeout=30,
    )
    return response.json()
