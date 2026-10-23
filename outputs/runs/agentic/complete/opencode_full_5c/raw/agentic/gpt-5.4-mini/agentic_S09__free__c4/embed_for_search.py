from embeddings_client import get_embeddings_client, embedding_model
from embeddings_models import EmbeddingRequest, embeddings_to_vectors


def embed_for_search(query, documents):
    client = get_embeddings_client()
    items = [query] + list(documents)
    response = client.embeddings.create(model=embedding_model(), input=items)
    vectors = embeddings_to_vectors(response)
    return {'query_embedding': vectors[0], 'document_embeddings': vectors[1:]}
