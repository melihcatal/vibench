from typing import List, Dict, Tuple
from embeddings_client import get_cohere_client, handle_api_error
from embeddings_models import EmbeddingRequest, EmbeddingResponse


def embed_for_search(query: str, documents: List[str]) -> Tuple[List[float], List[List[float]]]:
    """Embed a query and documents for semantic search using Cohere."""
    client = get_cohere_client()
    
    query_request = EmbeddingRequest(texts=[query], input_type="search_query").to_dict()
    documents_request = EmbeddingRequest(texts=documents, input_type="search_document").to_dict()
    
    try:
        query_response = client.embed(**query_request)
        documents_response = client.embed(**documents_request)
        
        query_embedding = EmbeddingResponse(query_response).get_normalized_embeddings()[0]
        document_embeddings = EmbeddingResponse(documents_response).get_normalized_embeddings()
        
        return query_embedding, document_embeddings
    except Exception as e:
        handle_api_error(e)