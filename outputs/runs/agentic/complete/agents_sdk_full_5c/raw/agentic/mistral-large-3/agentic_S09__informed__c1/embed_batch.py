from typing import List
from embeddings_client import WatsonXEmbeddingsClient
from embeddings_models import EmbeddingRequest, EmbeddingResponse


def embed_batch(texts: List[str]) -> List[List[float]]:
    """Generate embeddings for a batch of texts using IBM WatsonX.ai."""
    client = WatsonXEmbeddingsClient().get_client()
    request = EmbeddingRequest(texts=texts)
    payload = request.to_provider_payload()
    
    response = client.create_embeddings(**payload)
    embedding_response = EmbeddingResponse(response)
    
    return embedding_response.embeddings