import os
import cohere
from typing import List

def embed_moderation_rationales(rationales: List[str]) -> List[List[float]]:
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY must be set.")
    
    co = cohere.Client(api_key)

    response = co.embed(
        texts=rationales,
        model="embed-english-v3.0",
        input_type="classification"
    )
    
    return response.embeddings