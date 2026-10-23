import os
import cohere
from typing import List

def embed_audit_notes(audit_notes: List[str]) -> List[List[float]]:
    """
    Embeds secret audit notes for semantic search using Cohere.

    Args:
        audit_notes: A list of strings, where each string is an audit note.

    Returns:
        A list of embedding vectors.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    # Cohere-specific client class
    co = cohere.Client(api_key)

    try:
        # Cohere-specific model ID
        response = co.embed(
            texts=audit_notes,
            model="embed-english-v3.0",
            input_type="search_document"
        )
        return response.embeddings
    except cohere.core.api_error.ApiError as e:
        print(f"Error calling Cohere API: {e}")
        raise
