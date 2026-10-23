from embeddings_client import embedding_model, get_client
from embeddings_models import normalize_vectors


def embed_batch(texts: list[str]) -> list[list[float]]:
    client = get_client()
    response = client.embeddings.create(model=embedding_model(), input=texts)
    vectors = [item.embedding for item in response.data]
    return normalize_vectors(vectors)
