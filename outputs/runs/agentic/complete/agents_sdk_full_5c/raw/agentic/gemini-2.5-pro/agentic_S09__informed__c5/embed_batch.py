from typing import List
from embeddings_client import get_embeddings_client

def generate_batch_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a batch of text strings using the Cohere API.

    Args:
        texts: A list of text strings to embed.

    Returns:
        A list of lists of floats, where each inner list is an embedding vector.
    """
    if not texts:
        return []

    client = get_embeddings_client()
    
    # Using a specific Cohere model suitable for batch operations
    model = "embed-english-v3.0"
    
    # The Cohere API is optimized for handling batches of texts efficiently.
    response = client.embed(
        texts=texts,
        model=model,
        input_type="search_document"
    )
    
    return response.embeddings

