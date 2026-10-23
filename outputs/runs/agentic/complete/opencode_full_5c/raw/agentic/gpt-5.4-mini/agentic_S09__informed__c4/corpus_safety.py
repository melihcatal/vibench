import os

import requests


def check_corpus_text(text: str):
    endpoint = os.getenv("TISANE_ENDPOINT", "https://api.tisane.ai/parse")
    headers = {"X-Api-Key": os.getenv("TISANE_API_KEY", "")}
    response = requests.post(
        endpoint, json={"content": text, "language": "en"}, headers=headers, timeout=30
    )
    response.raise_for_status()
    return response.json()
