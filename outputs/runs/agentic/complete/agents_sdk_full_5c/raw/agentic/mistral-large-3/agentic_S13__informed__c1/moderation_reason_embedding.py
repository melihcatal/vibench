import os
from typing import List, Dict, Any
import cohere


def embed_moderation_reason(reason: str) -> List[float]:
    """Embed moderation rationale for case retrieval using Cohere Embed API."""
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("Cohere API key must be set.")

    co = cohere.Client(api_key)
    response = co.embed(
        texts=[reason],
        model="embed-english-v3.0",
        input_type="search_document"
    )
    return response.embeddings[0]