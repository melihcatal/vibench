from embeddings_client import get_client, embeddings_model
from embeddings_models import normalize_vector


def embed_for_search(query: str, documents):
    client = get_client()
    response = client.embeddings.create(model=embeddings_model(), input=[query, *documents])
    query_vector = normalize_vector(response.data[0].embedding)
    document_vectors = [normalize_vector(item.embedding) for item in response.data[1:]]
    return query_vector, document_vectors
