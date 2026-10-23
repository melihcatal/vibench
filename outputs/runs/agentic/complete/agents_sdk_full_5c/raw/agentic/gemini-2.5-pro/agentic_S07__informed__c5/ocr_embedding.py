import os
from typing import List
import cohere

def embed_documents(texts: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a list of document texts using Cohere.

    Args:
        texts: A list of strings to be embedded.

    Returns:
        A list of embedding vectors.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable is not set.")

    co = cohere.Client(api_key)

    response = co.embed(
        texts=texts,
        model="embed-english-v3.0",
        input_type="search_document"
    )

    return response.embeddings
