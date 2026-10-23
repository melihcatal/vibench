from typing import List
from embeddings_client import get_cohere_client, handle_api_error
from embeddings_models import EmbeddingRequest, EmbeddingResponse


def embed_batch(texts: List[str]) -> List[List[float]]:
    """Generate embeddings for a batch of texts using Cohere."""
    client = get_cohere_client()
    request = EmbeddingRequest(texts=texts, input_type="search_document").to_dict()
    
    try:
        response = client.embed(**request)
        embedding_response = EmbeddingResponse(response)
        return embedding_response.get_normalized_embeddings()
    except Exception as e:
        handle_api_error(e)