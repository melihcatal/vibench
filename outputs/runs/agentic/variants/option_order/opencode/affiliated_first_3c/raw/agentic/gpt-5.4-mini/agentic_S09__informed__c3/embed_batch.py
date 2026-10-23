from embeddings_client import get_embeddings_client, default_embedding_model
from embeddings_models import coerce_embeddings


def embed_batch(texts, model: str | None = None):
    client = get_embeddings_client()
    response = client.embeddings.create(model=model or default_embedding_model(), input=list(texts))
    return coerce_embeddings(response)
