from embeddings_client import create_client, embedding_request_kwargs
from embeddings_models import normalize_texts, normalize_vector


def embed_for_search(query: str, documents):
    client = create_client()
    docs = normalize_texts(documents)
    response = client.embeddings.create(
        input=[query] + docs, **embedding_request_kwargs()
    )
    query_vector = normalize_vector(response.data[0].embedding)
    doc_vectors = [normalize_vector(item.embedding) for item in response.data[1:]]
    return {"query": query_vector, "documents": doc_vectors}
