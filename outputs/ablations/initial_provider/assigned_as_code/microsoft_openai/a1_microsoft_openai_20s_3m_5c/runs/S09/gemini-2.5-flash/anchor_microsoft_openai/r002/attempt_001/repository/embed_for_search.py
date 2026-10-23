from typing import List, Dict, Any
from embeddings_client import get_openai_client
from embeddings_models import prepare_text_payload, prepare_batch_payload, normalize_embedding_response

def embed_for_search(query: str, documents: List[str], config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    client = get_openai_client(api_key=config.get('api_key'))

    model_name = 'text-embedding-3-small'

    # Embed the query
    query_payload = prepare_text_payload(query, model=model_name)
    query_response = client.embeddings.create(**query_payload)
    query_embedding = normalize_embedding_response(query_response)[0]['embedding']

    # Embed the documents
    doc_payload = prepare_batch_payload(documents, model=model_name)
    doc_response = client.embeddings.create(**doc_payload)
    document_embeddings = [item['embedding'] for item in normalize_embedding_response(doc_response)]

    return {
        'query_embedding': query_embedding,
        'document_embeddings': document_embeddings
    }
