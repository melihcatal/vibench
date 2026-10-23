from embeddings_client import client
from embeddings_models import EmbeddingRequest, normalize_response

def embed_for_search(query: str, documents: List[str]):
    query_embedding = client.embeddings.create(input=query, model='text-embedding-ada-002')
    document_embeddings = client.embeddings.create(input=documents, model='text-embedding-ada-002')
    query_embedding = normalize_response(query_embedding['data'][0])
    document_embeddings = [normalize_response(doc) for doc in document_embeddings['data']]
    return query_embedding, document_embeddings