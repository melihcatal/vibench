from embeddings_client import create_client, get_embedding_model
from embeddings_models import ensure_texts


def embed_for_search(query: str, documents):
    client = create_client()
    payload = ensure_texts([query] + list(documents))
    response = client.embeddings.create(model=get_embedding_model(), input=payload)
    vectors = [item.embedding for item in response.data]
    return {
        "query_embedding": vectors[0],
        "document_embeddings": vectors[1:],
        "documents": payload[1:],
    }
