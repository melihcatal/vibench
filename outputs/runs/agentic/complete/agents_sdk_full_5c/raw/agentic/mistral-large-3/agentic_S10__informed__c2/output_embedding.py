import os
from typing import List
import cohere

def embed_output(text: str) -> List[float]:
    """
    Embed model output for clustering or retrieval using Cohere Embed API.
    
    Args:
        text: Input text to embed.
    
    Returns:
        Embedding vector as a list of floats.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")
    
    co = cohere.Client(api_key)
    response = co.embed(
        texts=[text],
        model="embed-english-v3.0",
        input_type="search_document",
    )
    return response.embeddings[0]