from embeddings_client import cohere_client
from embeddings_models import cosine_similarity
import numpy as np

def calculate_similarity(text1: str, text2: str) -> float:
    """
    Calculates the cosine similarity between the embeddings of two texts.
    
    Args:
        text1: The first text string.
        text2: The second text string.
        
    Returns:
        The cosine similarity score.
    """
    # Provider-specific model ID: embed-english-v3.0
    response = cohere_client.embed(
        texts=[text1, text2],
        model='embed-english-v3.0',
        input_type='search_document'
    )
    
    embedding1 = np.array(response.embeddings[0])
    embedding2 = np.array(response.embeddings[1])
    
    return cosine_similarity(embedding1, embedding2)
