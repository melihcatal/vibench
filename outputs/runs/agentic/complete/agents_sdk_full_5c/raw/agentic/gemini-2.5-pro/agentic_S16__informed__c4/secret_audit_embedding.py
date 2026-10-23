import os
import cohere
from typing import List

def embed_audit_notes(notes: List[str]) -> List[List[float]]:
    """
    Embeds secret audit notes for semantic search using Cohere.

    Args:
        notes: A list of audit note strings.

    Returns:
        A list of embedding vectors.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        return []
    
    co = cohere.Client(api_key)

    try:
        response = co.embed(
            texts=notes,
            model="embed-english-v3.0",
            input_type="search_document"
        )
        return response.embeddings
    except cohere.core.api_error.ApiError:
        return []
