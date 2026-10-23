import os
from typing import List
import cohere

def embed_segments(segments: List[str], model_name: str = "embed-english-v3.0") -> List[List[float]]:
    """
    Generates embeddings for a list of text segments using Cohere's Embed API.
    """
    client = cohere.Client(os.environ.get("COHERE_API_KEY"))
    
    if not segments:
        return []

    response = client.embed(
        texts=segments,
        model=model_name,
        input_type="search_document"
    )
    
    return response.embeddings
