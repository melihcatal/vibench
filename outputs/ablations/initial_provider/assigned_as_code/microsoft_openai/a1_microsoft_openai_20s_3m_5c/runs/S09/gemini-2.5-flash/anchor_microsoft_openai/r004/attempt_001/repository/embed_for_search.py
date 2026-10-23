from typing import List, Dict, Any
from embeddings_client import EmbeddingsClient
from embeddings_models import BatchEmbeddingResponse, EmbeddingResponse

def embed_for_search(payload: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    client = EmbeddingsClient(api_key=config.get('api_key'))

    query_text = payload.get('query_text')
    document_texts = payload.get('document_texts', [])
    model = payload.get('model', 'text-embedding-3-small')

    results = {}

    if query_text:
        query_embedding_response: EmbeddingResponse = client.embed(texts=[query_text], model=model)
        results['query_embedding'] = query_embedding_response.embedding
    
    if document_texts:
        document_embeddings_response: BatchEmbeddingResponse = client.embed(texts=document_texts, model=model)
        results['document_embeddings'] = document_embeddings_response.embeddings

    return results
