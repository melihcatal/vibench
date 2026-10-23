from embeddings_client import cohere_client
from embeddings_models import EmbeddingResponse
from typing import List

MODEL_NAME = "embed-english-v3.0"

def generate_embeddings_batch(texts: List[str]) -> EmbeddingResponse:
    """
    Generates embeddings for a batch of text strings.
    """
    if not texts or not isinstance(texts, list):
        raise ValueError("Input texts must be a non-empty list of strings.")

    response = cohere_client.embed(
        texts=texts,
        model=MODEL_NAME,
        input_type="search_document"
    )
    
    return EmbeddingResponse(embeddings=response.embeddings, model=MODEL_NAME)
