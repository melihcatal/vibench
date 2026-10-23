import os
from typing import List, Optional
import cohere


def embed_output(
    text: str,
    model_id: str = "embed-english-v3.0"
) -> Optional[List[float]]:
    """
    Embed model outputs for clustering or retrieval using Cohere Embed API.
    
    Args:
        text: Text to embed.
        model_id: Cohere embedding model identifier.
        
    Returns:
        List of embedding floats or None if failed.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        return None

    co = cohere.Client(api_key)
    try:
        response = co.embed(
            texts=[text],
            model=model_id,
            input_type="search_document"
        )
        return response.embeddings[0] if response.embeddings else None
    except Exception:
        return None