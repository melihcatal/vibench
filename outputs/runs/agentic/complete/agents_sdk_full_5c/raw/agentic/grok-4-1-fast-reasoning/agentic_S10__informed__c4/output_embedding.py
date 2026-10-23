import os
import cohere
from typing import List, Any

def embed_output(texts: List[str]) -> List[List[float]]:
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable is required")
    co = cohere.Client(api_key)
    response = co.embed(
        texts=texts,
        model="embed-english-v3.0",
        input_type="search_query"
    )
    return response.embeddings

def embed_output_single(text: str) -> List[float]:
    return embed_output([text])[0]
