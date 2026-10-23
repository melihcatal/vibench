import os
import cohere
from typing import List
from security_models import EmbeddingRequest


def embed_audit_notes(request: EmbeddingRequest) -> List[List[float]]:
    """
    Generates embeddings for crypto audit notes for semantic search.

    Args:
        request: An EmbeddingRequest with the texts to embed.

    Returns:
        A list of embeddings for the provided texts.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    try:
        response = co.embed(
            texts=request.texts,
            model=request.model,
            input_type=request.input_type,
        )
        return response.embeddings
    except cohere.core.api_error.ApiError as e:
        print(f"An error occurred with the Cohere API: {e}")
        raise
