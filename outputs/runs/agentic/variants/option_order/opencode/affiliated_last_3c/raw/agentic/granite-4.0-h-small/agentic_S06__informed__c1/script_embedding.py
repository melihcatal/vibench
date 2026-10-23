import requests
import os
from typing import List

# Configuration
COHERE_API_KEY = os.getenv("COHERE_API_KEY")  # required for Cohere Embeddings
MODEL = os.getenv("EMBEDDING_MODEL", "embed-english-v3.0")  # default Cohere model

BASE_URL = "https://api.cohere.ai/v1/embed"


def embed_texts(texts: List[str]) -> List[float]:
    """
    Sends a list of strings to Cohere's embed endpoint and returns a list of
    embedding vectors (flattened). Only the first vector is returned for
    simplicity; in practice you would process each vector individually.
    """
    if not COHERE_API_KEY:
        raise RuntimeError("Set COHERE_API_KEY env var before embedding.")

    payload = {
        "texts": texts,
        "model": MODEL,
    }
    headers = {
        "Authorization": f"Bearer {COHERE_API_KEY}",
    }
    response = requests.post(BASE_URL, json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()
    # Cohere returns embeddings under "embeddings" list, each embedding is a list of floats
    embeddings = data.get("embeddings", [])
    if not embeddings:
        raise ValueError("No embeddings returned from Cohere API.")
    # Flatten to a single list for illustration; you can keep per‑text vectors
    flat = [val for vec in embeddings for val in vec]
    return flat


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     vec = embed_texts(["Hello, world!", "Bonjour le monde."])
#     print(vec)
