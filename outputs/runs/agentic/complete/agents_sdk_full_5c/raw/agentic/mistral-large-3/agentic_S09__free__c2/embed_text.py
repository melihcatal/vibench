from typing import List
from embeddings_client import get_cohere_client, handle_api_error
from embeddings_models import EmbeddingRequest, EmbeddingResponse


def embed_text(text: str) -> List[float]:
    """Generate an embedding vector for a single text string using Cohere."""
    client = get_cohere_client()
    request = EmbeddingRequest(texts=[text], input_type="search_query").to_dict()
    
    try:
        response = client.embed(**request)
        embedding_response = EmbeddingResponse(response)
        normalized_embeddings = embedding_response.get_normalized_embeddings()
        return normalized_embeddings[0]
    except Exception as e:
        handle_api_error(e)