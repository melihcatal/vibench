import os
from typing import List
import cohere

def embed_transcript_segments(segments: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a list of transcript segments using Cohere.

    Args:
        segments: A list of text strings (transcript segments).

    Returns:
        A list of embedding vectors.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    response = co.embed(
        texts=segments,
        model="embed-english-v3.0",
        input_type="search_document"
    )

    return response.embeddings
