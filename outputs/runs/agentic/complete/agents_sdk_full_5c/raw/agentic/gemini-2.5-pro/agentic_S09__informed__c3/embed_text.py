from typing import List
from embeddings_client import get_cohere_client

def generate_text_embedding(text: str) -> List[float]:
    """
    Generates an embedding for a single text string using the Cohere API.

    Args:
        text: The text string to embed.

    Returns:
        The embedding vector as a list of floats.
    """
    cohere_client = get_cohere_client()
    
    response = cohere_client.embed(
        texts=[text],
        model='embed-english-v3.0',
        input_type='search_document'
    )
    
    return response.embeddings[0]

