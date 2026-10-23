from typing import List
from embeddings_client import get_cohere_client
from embeddings_models import EmbeddingResponse


def generate_batch_embeddings(texts: List[str]) -> EmbeddingResponse:
    """
    Generates embeddings for a batch of texts using Cohere.
    """
    cohere_client = get_cohere_client()
    response = cohere_client.embed(
        texts=texts, model="embed-english-v3.0", input_type="search_document"
    )
    return EmbeddingResponse(embeddings=response.embeddings)
