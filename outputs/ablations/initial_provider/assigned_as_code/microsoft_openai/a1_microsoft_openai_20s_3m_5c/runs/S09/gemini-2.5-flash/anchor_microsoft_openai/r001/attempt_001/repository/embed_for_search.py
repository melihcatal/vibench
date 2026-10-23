from embeddings_client import EmbeddingsClient
from embeddings_models import EMBEDDING_MODEL

def embed_for_search(payload, config=None):
    client = EmbeddingsClient(api_key=config.get('api_key') if config else None).get_client()

    query_embedding_response = client.embeddings.create(model=EMBEDDING_MODEL, input=payload['query'])
    query_embedding = query_embedding_response.data[0].embedding

    document_embeddings_response = client.embeddings.create(model=EMBEDDING_MODEL, input=payload['documents'])
    document_embeddings = [item.embedding for item in document_embeddings_response.data]

    return {
        'query_embedding': query_embedding,
        'document_embeddings': document_embeddings
    }
