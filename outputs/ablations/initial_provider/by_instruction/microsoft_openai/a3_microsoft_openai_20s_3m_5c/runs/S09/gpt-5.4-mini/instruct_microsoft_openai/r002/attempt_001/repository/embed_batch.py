from embeddings_client import get_client, embeddings_model
from embeddings_models import normalize_vector


def embed_batch(texts):
    response = get_client().embeddings.create(model=embeddings_model(), input=texts)
    return [normalize_vector(item.embedding) for item in response.data]
