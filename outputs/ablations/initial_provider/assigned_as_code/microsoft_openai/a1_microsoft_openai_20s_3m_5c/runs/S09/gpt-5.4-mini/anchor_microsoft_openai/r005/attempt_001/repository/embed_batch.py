from embeddings_client import get_embeddings_model, get_openai_client
from embeddings_models import embedding_vectors_from_response, normalize_texts


def embed_batch(payload, config=None):
    config = config or {}
    texts = normalize_texts(payload)
    with get_openai_client(config) as client:
        response = client.embeddings.create(model=get_embeddings_model(config), input=texts)
    return {'embeddings': embedding_vectors_from_response(response)}
