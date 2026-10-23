from embeddings_client import EmbeddingsClient
from embeddings_models import SearchRequest, SearchResponse
from typing import List, Dict, Any

def embed_for_search(payload: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    client = EmbeddingsClient(api_key=config.get("api_key"))
    request = SearchRequest(
        query=payload["query"],
        documents=payload["documents"],
        model=payload.get("model", "text-embedding-3-small")
    )
    response = client.embed_for_search(request)
    return {
        "query_embedding": response.query_embedding,
        "document_embeddings": response.document_embeddings
    }
