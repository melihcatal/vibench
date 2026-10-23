from embeddings_client import DEFAULT_EMBEDDING_MODEL, get_client
from embeddings_models import normalize_texts, normalize_vector


def embed_batch(texts: list[str]) -> list[list[float]]:
    client = get_client()
    cleaned = normalize_texts(texts)
    response = client.embeddings.create(model=DEFAULT_EMBEDDING_MODEL, input=cleaned)
    return [normalize_vector(item.embedding) for item in response.data]
