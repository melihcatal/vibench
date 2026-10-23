import os
import cohere
from typing import List, Any

def transcript_embedding(texts: List[str]) -> List[List[float]]:
    """
    Embed transcript segments for semantic retrieval using Cohere.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable is not set")
    
    co = cohere.Client(api_key)
    response = co.embed(
        texts=texts,
        model="embed-english-v3.0",
        input_type="search_query"
    )
    return response.embeddings
