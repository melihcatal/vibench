import os
import cohere
from typing import List

def embed_moderation_reasons(reasons: List[str]) -> List[List[float]]:
    """
    Embeds moderation rationale text for finding similar past cases.

    Args:
        reasons: A list of strings, where each string is a rationale for a moderation decision.

    Returns:
        A list of embedding vectors.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")
        
    co = cohere.Client(api_key)

    try:
        response = co.embed(
            texts=reasons,
            model="embed-english-v3.0",
            input_type="search_document"
        )
        return response.embeddings
    except cohere.core.api_error.ApiError as e:
        print(f"Cohere API error: {e}")
        return []

