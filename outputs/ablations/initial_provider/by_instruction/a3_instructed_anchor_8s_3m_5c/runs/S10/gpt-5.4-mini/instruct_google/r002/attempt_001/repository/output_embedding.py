from typing import List

import requests


def output_embedding(text: str, api_key: str, model: str = "text-embedding-004") -> List[float]:
    response = requests.post(
        "https://generativelanguage.googleapis.com/v1beta/models/text-embedding-004:embedContent",
        params={"key": api_key},
        headers={"Content-Type": "application/json"},
        json={"content": {"parts": [{"text": text}]}},
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data.get("embedding", {}).get("values", [])
