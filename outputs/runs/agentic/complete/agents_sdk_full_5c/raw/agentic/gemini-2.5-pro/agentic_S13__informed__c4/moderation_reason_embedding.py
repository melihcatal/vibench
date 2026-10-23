import os
import cohere
from typing import List, Optional

def embed_moderation_reasons(reasons: List[str]) -> Optional[List[List[float]]]:
    """
    Generates embeddings for a list of moderation rationales using Cohere.

    Args:
        reasons: A list of text strings, where each string is a rationale.

    Returns:
        A list of embedding vectors, or None if an error occurs.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")
    
    co = cohere.Client(api_key)

    try:
        response = co.embed(
            texts=reasons,
            model='embed-english-v3.0',
            input_type='search_document'
        )
        return response.embeddings
    except cohere.CohereError as e:
        print(f"An error occurred with the Cohere API: {e}")
        return None
