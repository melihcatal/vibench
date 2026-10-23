import os
from typing import List
import cohere

def get_translation_memory_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a list of translated text segments using Cohere.

    These embeddings can be stored in a vector database for translation memory searches.

    Args:
        texts: A list of translated strings.

    Returns:
        A list of embedding vectors.
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
