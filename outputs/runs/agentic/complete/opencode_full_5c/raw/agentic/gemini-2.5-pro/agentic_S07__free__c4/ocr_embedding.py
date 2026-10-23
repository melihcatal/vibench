import os
import cohere
from typing import List


def get_text_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a list of text strings using Cohere.

    Args:
        texts: A list of strings to be embedded.

    Returns:
        A list of embedding vectors.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    # Provider-specific client
    co = cohere.Client(api_key)

    # Provider-specific model ID and API call
    model_name = "embed-english-v3.0"

    response = co.embed(texts=texts, model=model_name, input_type="search_document")

    return response.embeddings
