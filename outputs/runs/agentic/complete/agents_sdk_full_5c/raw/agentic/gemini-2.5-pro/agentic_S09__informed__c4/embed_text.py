from embeddings_client import cohere_client
from typing import List

def generate_text_embedding(text: str) -> List[float]:
    """
    Generates an embedding for a single text string using Cohere API.
    
    Args:
        text: The text string to embed.
        
    Returns:
        The embedding vector.
    """
    # Provider-specific model ID: embed-english-v3.0
    response = cohere_client.embed(
        texts=[text],
        model='embed-english-v3.0',
        input_type='search_document'
    )
    return response.embeddings[0]
