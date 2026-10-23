import os
import requests
from typing import List, Any

# Voyage AI provider
VOYAGE_API_KEY = os.getenv("VOYAGE_API_KEY")

def log_embedding(texts: List[str], model: str = "voyage-2") -> List[List[float]]:
    """
    Embed selected log messages for semantic retrieval using Voyage AI.
    """
    url = "https://api.voyageai.com/v1/embeddings"
    headers = {
        "Authorization": f"Bearer {VOYAGE_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "input": texts
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()["data"]
    return [item["embedding"] for item in data]