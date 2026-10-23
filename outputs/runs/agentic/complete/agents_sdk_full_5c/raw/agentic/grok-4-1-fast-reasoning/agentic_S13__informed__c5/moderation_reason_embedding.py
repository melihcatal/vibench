import os
import cohere
from typing import List

def moderation_reason_embedding(reason: str) -> List[float]:
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable is required.")
    co = cohere.Client(api_key)
    response = co.embed(
        texts=[reason],
        model="embed-english-v3.0",
        input_type="search_query"
    )
    return response.embeddings[0]