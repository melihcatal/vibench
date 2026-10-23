from typing import List
import os
import cohere
from .model_models import EmbeddingRequest, EmbeddingResponse


def platform_output_embedding(texts: List[str]) -> EmbeddingResponse:
    """
    Embeds platform outputs for evaluation or retrieval using Cohere Embed API.
    """
    co = cohere.Client(os.getenv("COHERE_API_KEY"))

    response = co.embed(
        texts=texts, model="embed-english-v3.0", input_type="search_document"
    )

    return EmbeddingResponse(embeddings=response.embeddings, model="embed-english-v3.0")
