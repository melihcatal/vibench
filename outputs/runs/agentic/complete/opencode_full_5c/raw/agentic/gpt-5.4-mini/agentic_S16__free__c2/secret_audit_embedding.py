import os
from typing import List

import requests


def secret_audit_embedding(text: str) -> List[float]:
    api_key = os.environ.get("OPENAI_API_KEY", "")
    response = requests.post(
        "https://api.openai.com/v1/embeddings",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={"model": "text-embedding-3-small", "input": text},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["data"][0]["embedding"]


if __name__ == "__main__":
    print(secret_audit_embedding("rotation audit note"))
