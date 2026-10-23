import json
import os

import requests

from security_client import load_security_config
from security_models import normalize_text


OPENAI_EMBEDDINGS_URL = "https://api.openai.com/v1/embeddings"


def crypto_audit_embedding(note: str) -> dict:
    config = load_security_config()
    response = requests.post(OPENAI_EMBEDDINGS_URL, headers={"Authorization": f"Bearer {config['openai_api_key']}", "Content-Type": "application/json"}, json={"model": "text-embedding-3-large", "input": normalize_text(note)}, timeout=60)
    response.raise_for_status()
    data = response.json()
    return {"provider": "openai", "embedding": data.get("data", [{}])[0].get("embedding", []), "note": normalize_text(note)}


if __name__ == "__main__":
    print(json.dumps(crypto_audit_embedding(normalize_text(os.getenv("NOTE", "")))))
