import os
import cohere
from typing import List


def ocr_embedding(texts: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a list of text chunks using the Cohere API.

    Args:
        texts (List[str]): A list of strings to be embedded.

    Returns:
        List[List[float]]: A list of embedding vectors.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    response = co.embed(
        texts=texts,
        model="embed-english-v3.0",
        input_type="search_document",
    )

    return response.embeddings
