import cohere
from typing import List
from translation_client import COHERE_API_KEY

def embed_translated_segments(segments: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a list of translated text segments using Cohere.

    This is useful for building a translation memory or for semantic search
    on translated content.

    Args:
        segments: A list of text strings to embed.

    Returns:
        A list of embeddings, where each embedding is a list of floats.
    """
    if not COHERE_API_KEY:
        raise ValueError("COHERE_API_KEY environment variable is not set.")

    co = cohere.Client(COHERE_API_KEY)

    response = co.embed(
        texts=segments,
        model='embed-english-v3.0', # Provider-specific model ID
        input_type='search_document'
    )

    return response.embeddings
