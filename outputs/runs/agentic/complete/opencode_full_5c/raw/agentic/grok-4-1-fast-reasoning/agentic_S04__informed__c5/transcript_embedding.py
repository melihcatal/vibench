import os
from typing import List
import cohere


def transcript_embedding(segments: List[str]) -> List[List[float]]:
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY not set")
    co = cohere.Client(api_key)
    response = co.embed(texts=segments, model="embed-english-v3.0")
    return response.embeddings
