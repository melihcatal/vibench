from typing import List, Dict, Any

from embeddings_client import get_embeddings_client
from embeddings_models import BatchEmbeddingsResponse, normalize_batch_embedding_response

def embed_for_search(payload: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    query = payload.get("query")
    documents = payload.get("documents", [])

    if not query:
        raise ValueError("Payload must contain a 'query' string.")
    if not documents:
        raise ValueError("Payload must contain a 'documents' key with a list of strings.")
    
    all_texts = [query] + documents

    client = get_embeddings_client(api_key=config.get("api_key"))

    response = client.models.embed_content(model="gemini-embedding-001", contents=all_texts)

    normalized_response = normalize_batch_embedding_response(response)
    
    # The first embedding is for the query, the rest are for documents
    query_embedding = normalized_response.embeddings[0]
    document_embeddings = normalized_response.embeddings[1:]

    return {"query_embedding": query_embedding, "document_embeddings": document_embeddings}
