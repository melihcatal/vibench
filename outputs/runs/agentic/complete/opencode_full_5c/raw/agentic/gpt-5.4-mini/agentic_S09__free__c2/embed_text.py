from embeddings_client import DEFAULT_EMBEDDING_MODEL, get_client
from embeddings_models import normalize_vector


def embed_text(text: str) -> list[float]:
    client = get_client()
    response = client.embeddings.create(model=DEFAULT_EMBEDDING_MODEL, input=text)
    return normalize_vector(response.data[0].embedding)
