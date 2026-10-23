import os
from typing import List
import cohere

def embed_script(
    text: str,
    model: str = "embed-english-v3.0"
) -> List[float]:
    """
    Embed narration scripts for voice-asset search using Cohere Embed API.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("Cohere API key must be provided.")
    
    co = cohere.Client(api_key)
    response = co.embed(
        texts=[text],
        model=model,
        input_type="search_document"
    )
    
    return response.embeddings[0]