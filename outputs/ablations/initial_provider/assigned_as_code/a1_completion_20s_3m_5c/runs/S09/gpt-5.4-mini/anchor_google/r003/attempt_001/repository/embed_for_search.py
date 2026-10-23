from embeddings_client import get_model, make_client
from embeddings_models import embedding_vectors, normalize_texts


def embed_for_search(payload, config=None):
    texts = normalize_texts(payload)
    with make_client(config) as client:
        response = client.models.embed_content(model=get_model(config), contents=texts)
    vectors = embedding_vectors(response)
    return {"query_embedding": vectors[0], "document_embeddings": vectors[1:]}
