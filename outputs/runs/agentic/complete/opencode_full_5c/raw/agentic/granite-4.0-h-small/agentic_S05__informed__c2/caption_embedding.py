import numpy as np
import requests

COHERE_EMBED_ENDPOINT = "https://api.cohere.com/v1/embed"

COHERE_API_KEY = "COHERE_API_KEY"


def embed_caption_chunk(text):
    """Embed caption chunks for semantic meeting search using Cohere Embed API."""
    payload = {"model": "embed-english-v3.0", "texts": [text]}
    headers = {
        "Authorization": f"Bearer {COHERE_API_KEY}",
        "Content-Type": "application/json",
    }
    r = requests.post(COHREE_EMBED_ENDPOINT, headers=headers, json=payload)
    r.raise_for_status()
    vec = r.json()["embeddings"][0]["data"]
    return np.array(vec, dtype=np.float32)


# Example usage: embed_caption_chunk('Speaker: Hello world.')
