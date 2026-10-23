import os
import cohere
from typing import List

def embed_moderation_rationale(rationale: str) -> List[float]:
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY must be set")
    co = cohere.Client(api_key)
    embedding = co.embed(
        texts=[rationale],
        model="embed-english-v3.0",
        input_type="search_query"
    )
    return embedding.embeddings[0]
