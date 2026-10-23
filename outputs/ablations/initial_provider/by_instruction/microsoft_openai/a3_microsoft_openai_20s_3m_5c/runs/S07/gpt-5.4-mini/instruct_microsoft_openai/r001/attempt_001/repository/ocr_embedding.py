import os

import requests


def embed_ocr_sections(sections):
    endpoint = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
    api_key = os.getenv("OPENAI_API_KEY", "")
    response = requests.post(
        f"{endpoint}/embeddings",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": "text-embedding-3-large", "input": sections},
        timeout=120,
    )
    response.raise_for_status()
    return response.json()
