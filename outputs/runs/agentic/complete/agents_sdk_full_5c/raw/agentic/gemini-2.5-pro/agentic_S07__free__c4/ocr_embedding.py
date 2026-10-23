import os
import cohere
from typing import List

def get_cohere_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a list of texts using Cohere's API.

    Args:
        texts: A list of strings to be embedded.

    Returns:
        A list of embedding vectors (each a list of floats).
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    try:
        response = co.embed(
            texts=texts,
            model="embed-english-v3.0",
            input_type="search_document"
        )
        return response.embeddings
    except cohere.CohereError as e:
        print(f"An error occurred with Cohere API: {e}")
        return []
