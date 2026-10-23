from typing import List
from embeddings_client import cohere_client


def embed_batch(texts: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a batch of texts using Cohere.
    """
    response = cohere_client.embed(
        texts=texts, model="embed-english-v3.0", input_type="search_document"
    )
    return response.embeddings
