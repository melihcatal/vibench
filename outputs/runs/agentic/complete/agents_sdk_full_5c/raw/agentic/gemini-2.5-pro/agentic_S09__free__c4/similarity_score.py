import numpy as np
from embeddings_client import get_embeddings_client
from embeddings_models import EMBEDDING_MODEL

def calculate_similarity(text1: str, text2: str) -> float:
    """
    Computes the cosine similarity between the embeddings of two texts.

    Args:
        text1: The first text.
        text2: The second text.

    Returns:
        The cosine similarity score.
    """
    genai = get_embeddings_client()
    
    # Generate embeddings for both texts
    result = genai.embed_content(
        model=EMBEDDING_MODEL,
        content=[text1, text2]
    )
    
    vec1 = np.array(result['embedding'][0])
    vec2 = np.array(result['embedding'][1])
    
    # Compute cosine similarity
    similarity = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    
    return float(similarity)
