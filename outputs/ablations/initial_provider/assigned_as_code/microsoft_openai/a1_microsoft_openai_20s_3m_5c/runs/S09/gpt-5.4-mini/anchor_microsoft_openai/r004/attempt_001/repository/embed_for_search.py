from embeddings_client import get_openai_client
from embeddings_models import extract_embedding_vector, extract_embeddings_vectors


def embed_for_search(payload, config=None):
    client, settings = get_openai_client(config)
    query_response = client.embeddings.create(model=settings['model'], input=payload['query'])
    document_response = client.embeddings.create(model=settings['model'], input=payload['documents'])
    return {
        'query_embedding': extract_embedding_vector(query_response),
        'document_embeddings': extract_embeddings_vectors(document_response),
    }
