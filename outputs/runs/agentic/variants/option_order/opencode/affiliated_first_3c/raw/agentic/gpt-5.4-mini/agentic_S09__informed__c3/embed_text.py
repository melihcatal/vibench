from embeddings_client import get_embeddings_client, default_embedding_model
from embeddings_models import coerce_single_embedding


def embed_text(text: str, model: str | None = None):
    client = get_embeddings_client()
    response = client.embeddings.create(model=model or default_embedding_model(), input=text)
    return coerce_single_embedding(response)
