import os
from typing import List
from embeddings_client import WatsonXEmbeddingsClient
from embeddings_models import EmbeddingRequest, EmbeddingResponse


def embed_text(text: str) -> List[float]:
    """Generate an embedding vector for a single text string using IBM WatsonX.ai."""
    client = WatsonXEmbeddingsClient().get_client()
    request = EmbeddingRequest(texts=[text])
    payload = request.to_provider_payload()
    
    response = client.create_embeddings(**payload)
    embedding_response = EmbeddingResponse(response)
    
    return embedding_response.embeddings[0]