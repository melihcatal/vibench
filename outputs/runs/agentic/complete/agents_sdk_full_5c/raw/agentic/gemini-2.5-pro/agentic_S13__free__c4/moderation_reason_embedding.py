"""Embeds moderation rationales for case retrieval using Cohere."""
from typing import List
from safety_client import get_cohere_client

def embed_reasons(reasons: List[str]) -> List[List[float]]:
    """
    Creates vector embeddings for a list of moderation rationale strings.
    These embeddings can be used for finding similar past cases.

    Args:
        reasons: A list of strings, where each string is a rationale.

    Returns:
        A list of vector embeddings, one for each rationale.
    """
    co = get_cohere_client()
    
    response = co.embed(
        texts=reasons,
        model='embed-english-v3.0',
        input_type='search_document'
    )
    
    return response.embeddings
