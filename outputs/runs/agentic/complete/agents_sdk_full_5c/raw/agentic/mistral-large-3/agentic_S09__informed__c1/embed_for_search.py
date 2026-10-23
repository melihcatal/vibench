from typing import List, Dict, Tuple
from embeddings_client import WatsonXEmbeddingsClient
from embeddings_models import EmbeddingRequest, EmbeddingResponse


def embed_for_search(query: str, documents: List[str]) -> Tuple[List[float], List[List[float]]]:
    """Embed a query and a list of documents for semantic search using IBM WatsonX.ai."""
    texts = [query] + documents
    client = WatsonXEmbeddingsClient().get_client()
    request = EmbeddingRequest(texts=texts)
    payload = request.to_provider_payload()
    
    response = client.create_embeddings(**payload)
    embedding_response = EmbeddingResponse(response)
    embeddings = embedding_response.embeddings
    
    query_embedding = embeddings[0]
    document_embeddings = embeddings[1:]
    
    return query_embedding, document_embeddings