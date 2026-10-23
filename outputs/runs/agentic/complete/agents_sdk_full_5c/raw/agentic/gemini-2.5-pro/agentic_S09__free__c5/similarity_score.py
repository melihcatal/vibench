import os
import numpy as np
from embeddings_client import get_embeddings_client
from embeddings_models import cosine_similarity

def calculate_similarity(text1: str, text2: str) -> float:
    """
    Calculates the cosine similarity between the embeddings of two texts.

    Args:
        text1: The first text.
        text2: The second text.

    Returns:
        The cosine similarity score.
    """
    if not all(isinstance(t, str) and t for t in [text1, text2]):
        raise ValueError("Both inputs must be non-empty strings.")

    client = get_embeddings_client()
    
    # Get embeddings for both texts in a single API call
    embeddings = client.get_embeddings([text1, text2])
    
    vec1 = np.array(embeddings[0].values)
    vec2 = np.array(embeddings[1].values)
    
    return cosine_similarity(vec1, vec2)
