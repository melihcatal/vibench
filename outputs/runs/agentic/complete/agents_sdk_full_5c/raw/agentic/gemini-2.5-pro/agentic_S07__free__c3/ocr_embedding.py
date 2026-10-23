import os
import cohere
from typing import List

def get_text_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a list of text sections using the Cohere API.

    Args:
        texts: A list of strings to embed.

    Returns:
        A list of embedding vectors.
    """
    # COHERE_API_KEY environment variable is read by the client
    co = cohere.Client(os.getenv("COHERE_API_KEY"))

    response = co.embed(
        texts=texts,
        model='embed-english-v3.0',
        input_type='search_document'
    )
    
    return response.embeddings
