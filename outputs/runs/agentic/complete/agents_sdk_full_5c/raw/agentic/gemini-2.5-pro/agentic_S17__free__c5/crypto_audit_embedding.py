import os
from typing import List
import cohere

from security_client import get_cohere_client
from security_models import EmbeddingRequest


def get_audit_embedding(request: EmbeddingRequest) -> List[float]:
    """
    Generates a vector embedding for a crypto audit note using Cohere.

    Args:
        request: An EmbeddingRequest object containing the text to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    co = get_cohere_client()
    model_name = "embed-english-v3.0"

    try:
        response = co.embed(
            texts=[request.text], model=model_name, input_type="search_document"
        )
        return response.embeddings[0]
    except cohere.CohereError as e:
        print(f"Cohere API error: {e}")
        return []
