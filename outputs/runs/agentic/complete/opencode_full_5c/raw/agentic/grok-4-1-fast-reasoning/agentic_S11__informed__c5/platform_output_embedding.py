import os
import cohere
from typing import List, float


def embed_platform_output(text: str) -> List[float]:
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY required")
    co = cohere.Cohere(api_key)
    response = co.embed(
        texts=[text],
        model="embed-english-v3.0",
    )
    return response.embeddings[0]
