from embeddings_client import cohere_client
from typing import List

def generate_batch_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a batch of text strings using Cohere API.
    
    Args:
        texts: A list of text strings to embed.
        
    Returns:
        A list of embedding vectors.
    """
    if not texts:
        return []

    # Provider-specific model ID: embed-english-v3.0
    response = cohere_client.embed(
        texts=texts,
        model='embed-english-v3.0',
        input_type='search_document'
    )
    return response.embeddings
