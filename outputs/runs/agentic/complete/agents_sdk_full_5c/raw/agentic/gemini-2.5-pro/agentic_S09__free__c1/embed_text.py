from typing import List
from embeddings_client import get_cohere_client

def generate_text_embedding(text: str) -> List[float]:
    """
    Generates an embedding vector for a single text string using Cohere.

    Args:
        text: The text string to embed.

    Returns:
        The embedding vector for the text.
    """
    cohere_client = get_cohere_client()
    
    # Using a model from the Cohere platform
    response = cohere_client.embed(
        texts=[text],
        model='embed-english-v3.0',
        input_type='search_document'
    )
    
    return response.embeddings[0]
