import os
import cohere
from typing import List

def embed_text_segments(segments: List[str]) -> List[List[float]]:
    """
    Creates embeddings for translated text segments for use in a translation memory system.

    Args:
        segments: A list of text strings to embed.

    Returns:
        A list of embedding vectors.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    co = cohere.Client(api_key)

    if not segments:
        return []

    response = co.embed(
        texts=segments,
        model='embed-english-v3.0', # Example model, can be multilingual
        input_type='search_document'
    )
    
    return response.embeddings
