import os
import cohere
from typing import List

def embed_translated_segment(text: str) -> List[float]:
    """
    Embeds a single translated text segment using Cohere's API.

    Args:
        text: The translated text segment to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")
        
    co = cohere.Client(api_key)

    response = co.embed(
        texts=[text],
        model='embed-english-v3.0',
        input_type='search_document'
    )
    
    return response.embeddings[0]

def embed_many_segments(texts: List[str]) -> List[List[float]]:
    """
    Embeds a batch of translated text segments using Cohere's API.

    Args:
        texts: A list of translated text segments to embed.

    Returns:
        A list of embedding vectors.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    response = co.embed(
        texts=texts,
        model='embed-english-v3.0',
        input_type='search_document'
    )

    return response.embeddings
