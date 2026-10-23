from typing import List, Dict
from embeddings_client import EmbeddingsClient
from embeddings_models import EmbeddingsModels

def embed_for_search(query: str, documents: List[str]) -> Dict[str, List[List[float]]]:
    """Embeds a query and a list of documents for semantic search using Google Vertex AI.

    Args:
        query: The search query string.
        documents: A list of document strings to embed.

    Returns:
        A dictionary containing 'query_embedding' and 'document_embeddings'.
    """
    client = EmbeddingsClient()
    
    all_texts = [query] + documents
    instances = EmbeddingsModels.prepare_instances(all_texts)
    
    response = client.get_client().predict(endpoint=client.get_endpoint(), instances=instances)
    
    all_embeddings = EmbeddingsModels.parse_response(response)
    
    query_embedding = all_embeddings[0]
    document_embeddings = all_embeddings[1:]
    
    return {"query_embedding": query_embedding, "document_embeddings": document_embeddings}
