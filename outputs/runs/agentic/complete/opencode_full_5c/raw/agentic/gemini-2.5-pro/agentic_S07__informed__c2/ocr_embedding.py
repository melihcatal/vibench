import os
import cohere
from typing import List


def get_text_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a list of texts using Cohere.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("Cohere API key must be set as COHERE_API_KEY")

    co = cohere.Client(api_key)

    response = co.embed(
        texts=texts, model="embed-english-v3.0", input_type="search_document"
    )

    return response.embeddings
