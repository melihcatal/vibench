from typing import List
from embeddings_client import cohere_client


def embed_text(text: str) -> List[float]:
    """
    Generates an embedding vector for one text string using Cohere.
    """
    response = cohere_client.embed(
        texts=[text], model="embed-english-v3.0", input_type="search_document"
    )
    return response.embeddings[0]
