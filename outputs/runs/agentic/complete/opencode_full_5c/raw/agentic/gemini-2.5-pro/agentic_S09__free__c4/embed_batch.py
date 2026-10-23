from typing import List
from embeddings_client import get_cohere_client
from embeddings_models import EmbeddingResponse


def embed_batch(texts: List[str]) -> EmbeddingResponse:
    """
    Generates embeddings for a batch of texts using Cohere API.
    """
    cohere_client = get_cohere_client()
    model = "embed-english-v3.0"
    response = cohere_client.embed(
        texts=texts, model=model, input_type="search_document"
    )
    return EmbeddingResponse(embeddings=response.embeddings, model=model)
