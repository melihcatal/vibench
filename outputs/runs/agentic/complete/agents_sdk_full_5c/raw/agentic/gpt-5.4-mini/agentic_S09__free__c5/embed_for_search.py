from embeddings_client import OPENAI_EMBEDDING_MODEL, get_client
from embeddings_models import EmbeddingResponse, normalize_vectors


def embed_for_search(query: str, documents, model: str = OPENAI_EMBEDDING_MODEL):
    client = get_client()
    payload = [query] + list(documents)
    response = client.embeddings.create(model=model, input=payload)
    vectors = [item.embedding for item in response.data]
    query_vector = normalize_vectors([vectors[0]])[0]
    document_vectors = normalize_vectors(vectors[1:])
    return EmbeddingResponse(model=response.model, vectors=[query_vector] + document_vectors)
