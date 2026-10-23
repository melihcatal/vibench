import os

import requests


def ocr_embedding(text):
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"].rstrip("/")
    key = os.environ["AZURE_OPENAI_API_KEY"]
    deployment = os.environ["AZURE_OPENAI_EMBEDDING_DEPLOYMENT"]
    url = f"{endpoint}/openai/deployments/{deployment}/embeddings?api-version=2024-02-15-preview"
    response = requests.post(
        url,
        headers={"api-key": key, "Content-Type": "application/json"},
        json={"input": text},
        timeout=60,
    )
    response.raise_for_status()
    return response.json()["data"][0]["embedding"]
