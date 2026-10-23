# output_embedding.py
# [LATER-STEP]
"""Embeds generated text output using a hosted embedding model.

Calls a concrete hosted embedding endpoint (e.g., OpenAI's text-embedding-ada-002)
to produce a vector representation useful for clustering, semantic search,
or downstream retrieval systems.

The function returns a NumPy array (or list) of float values.
"""

import os
import json
import numpy as np
import requests
from typing import List

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "demo_key")
BASE_URL = "https://api.openai.com/v1/embeddings"


def embed_text(text: str, model: str = "text-embedding-ada-002") -> List[float]:
    """
    Generates a vector embedding for the supplied text.

    Args:
        text (str): The string to embed.
        model (str): Identifier of the embedding model (default: ada-002).
    Returns:
        List[float]: Embedding vector as a list of floats.
    """
    payload = {
        "model": model,
        "input": text,
    }
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    resp = requests.post(BASE_URL, json=payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    # The API returns an array of embeddings under 'data'[0]['embedding']
    embedding = data["data"][0]["embedding"]
    return embedding  # type: ignore


# Demo (do not execute on import)
# if __name__ == '__main__':
#     vec = embed_text('Hello world')
#     print('Embedding shape:', len(vec))
