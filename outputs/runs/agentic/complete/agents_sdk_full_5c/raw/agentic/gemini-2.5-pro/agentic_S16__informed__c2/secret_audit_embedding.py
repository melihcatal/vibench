import os
import cohere
from typing import List

def embed_audit_notes(notes: List[str]) -> List[List[float]]:
    """
    Embeds secret audit notes for semantic search using Cohere's API.

    Args:
        notes: A list of strings, where each string is an audit note.

    Returns:
        A list of embeddings, one for each note.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    response = co.embed(
        texts=notes,
        model='embed-english-v3.0',
        input_type='search_document'
    )

    return response.embeddings
