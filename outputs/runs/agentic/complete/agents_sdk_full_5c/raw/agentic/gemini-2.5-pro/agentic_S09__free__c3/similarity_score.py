import numpy as np
from embeddings_client import get_cohere_client

def _calculate_cosine_similarity(vec1, vec2):
    """Helper to compute cosine similarity."""
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)

def calculate_text_similarity(text1: str, text2: str) -> float:
    """
    Computes the cosine similarity between the embeddings of two texts.

    Args:
        text1: The first text string.
        text2: The second text string.

    Returns:
        A float representing the cosine similarity score.
    """
    cohere_client = get_cohere_client()
    
    response = cohere_client.embed(
        texts=[text1, text2],
        model='embed-english-v3.0',
        input_type='search_document'
    )
    
    embedding1 = response.embeddings[0]
    embedding2 = response.embeddings[1]
    
    similarity = _calculate_cosine_similarity(embedding1, embedding2)
    
    return float(similarity)
