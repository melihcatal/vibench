from typing import List
from model_client import get_cohere_client
from model_models import EmbeddingResponse


def platform_output_embedding(texts: List[str]) -> EmbeddingResponse:
    """
    Embed platform outputs for evaluation or retrieval using Cohere's embedding models.
    """
    co = get_cohere_client()

    response = co.embed(
        texts=texts, model="embed-english-v3.0", input_type="search_document"
    )

    return EmbeddingResponse(embeddings=response.embeddings)
