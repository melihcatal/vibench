from typing import List
import os
import cohere


def embed_script(text: str, model: str = "embed-english-v3.0") -> List[float]:
    """
    Embed narration scripts for voice-asset search using Cohere.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set")
    
    co = cohere.Client(api_key)
    response = co.embed(texts=[text], model=model)
    
    return response.embeddings[0]