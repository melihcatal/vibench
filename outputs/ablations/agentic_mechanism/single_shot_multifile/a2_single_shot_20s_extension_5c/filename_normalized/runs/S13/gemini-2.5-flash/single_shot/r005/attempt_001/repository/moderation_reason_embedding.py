import os
import cohere
from safety_client import load_cohere_client
from safety_models import EmbeddingRequest

def embed_moderation_reason(embedding_request: EmbeddingRequest) -> list[float]:
    client = load_cohere_client()

    response = client.embed(
        texts=[embedding_request.text],
        model="embed-english-v3.0",
        input_type="search_document" # or "clustering", "classification", "retrieval_query", "retrieval_document"
    )

    if response.embeddings:
        return response.embeddings[0]
    return []
