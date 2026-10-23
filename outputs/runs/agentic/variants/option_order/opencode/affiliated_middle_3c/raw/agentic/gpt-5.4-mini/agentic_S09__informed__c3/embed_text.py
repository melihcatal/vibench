from embeddings_client import get_embeddings_client, default_embedding_model
from embeddings_models import single_embedding_response, normalize_text_input


def embed_text(text: str):
    client = get_embeddings_client()
    response = client.embeddings.create(model=default_embedding_model(), input=normalize_text_input(text))
    return single_embedding_response(response)
