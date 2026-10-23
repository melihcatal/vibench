import os
import cohere
from typing import List


def embed_scripts(texts: List[str]) -> List[List[float]]:
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY must be set in environment variables.")

    co = cohere.Client(api_key)
    response = co.embed(texts=texts, model="embed-english-v3.0")
    return response.embeddings