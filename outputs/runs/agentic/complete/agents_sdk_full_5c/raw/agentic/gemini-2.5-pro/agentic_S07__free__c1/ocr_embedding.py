import os
from typing import List
import cohere

def embed_text_sections(texts: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a list of text sections using Cohere.

    Requires the COHERE_API_KEY environment variable.

    Args:
        texts: A list of text strings to embed.

    Returns:
        A list of embeddings, where each embedding is a list of floats.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    response = co.embed(
        texts=texts,
        model="embed-english-v3.0",
        input_type="search_document"
    )

    return response.embeddings
