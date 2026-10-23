import os
import cohere
from typing import List

def embed_audit_notes(notes: List[str]) -> List[List[float]] | None:
    """
    Generates embeddings for secret audit notes using the Cohere API.

    These embeddings can be stored in a vector database for semantic search
    to find related audit events.

    Args:
        notes: A list of strings, where each string is an audit note.

    Returns:
        A list of embedding vectors, or None if an error occurs.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        print("COHERE_API_KEY environment variable must be set.")
        return None

    try:
        co = cohere.Client(api_key)
        
        response = co.embed(
            texts=notes,
            model="embed-english-v3.0",
            input_type="search_document"
        )
        
        return response.embeddings
        
    except Exception as e:
        print(f"An error occurred while generating embeddings with Cohere: {e}")
        return None

