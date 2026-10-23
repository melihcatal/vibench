import os
import cohere
from typing import List

def translation_memory_embedding(segments: List[str]) -> List[List[float]]:
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY not set")
    co = cohere.Client(api_key)
    response = co.embed(
        texts=segments,
        model="embed-english-v3.0",
        embedding_types=["FLOAT"]
    )
    return response.embeddings["FLOAT"]
