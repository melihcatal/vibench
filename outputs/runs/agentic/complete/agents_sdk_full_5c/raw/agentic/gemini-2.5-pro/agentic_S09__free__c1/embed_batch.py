from typing import List
from embeddings_client import get_cohere_client

def generate_batch_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a batch of texts using Cohere.

    Args:
        texts: A list of text strings to embed.

    Returns:
        A list of embedding vectors.
    """
    cohere_client = get_cohere_client()
    
    # Using a model from the Cohere platform for batch processing
    response = cohere_client.embed(
        texts=texts,
        model='embed-english-v3.0',
        input_type='search_document'
    )
    
    return response.embeddings
