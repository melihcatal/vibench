import os
import cohere
from typing import List, Any


def get_output_embedding(texts: List[str]) -> List[List[float]]:
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable is required")
    co = cohere.Client(api_key)
    response = co.embed(texts=texts, model="embed-english-v3.0")
    return response.embeddings


def get_output_embedding_single(text: str) -> List[float]:
    embeddings = get_output_embedding([text])
    return embeddings[0]
