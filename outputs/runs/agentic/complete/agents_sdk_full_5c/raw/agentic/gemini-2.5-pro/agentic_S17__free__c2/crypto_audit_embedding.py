from typing import List
from security_client import get_cohere_client

def embed_audit_notes_cohere(audit_notes: List[str]) -> List[List[float]]:
    """
    Generates embeddings for crypto audit notes using Cohere.

    Args:
        audit_notes: A list of strings, where each string is an audit note.

    Returns:
        A list of embedding vectors.
    """
    co = get_cohere_client()
    try:
        # Provider-specific call to Cohere's Embed API
        response = co.embed(
            texts=audit_notes,
            model="embed-english-v3.0",
            input_type="search_document"
        )
        return response.embeddings
    except Exception as e:
        print(f"Error generating embeddings with Cohere: {e}")
        return []
