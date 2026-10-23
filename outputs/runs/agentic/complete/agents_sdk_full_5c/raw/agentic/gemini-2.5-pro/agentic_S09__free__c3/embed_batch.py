from typing import List
from embeddings_client import get_cohere_client

def generate_batch_embeddings(texts: List[str]):
    """
    Generates embeddings for a batch of text strings.

    Args:
        texts: A list of text strings to embed.

    Returns:
        A list of embedding vectors (list of lists of floats).
    """
    cohere_client = get_cohere_client()
    
    response = cohere_client.embed(
        texts=texts,
        model='embed-english-v3.0',
        input_type='search_document'
    )
    
    return response.embeddings
