from embeddings_client import get_embeddings_client, default_embedding_model
from embeddings_models import batch_embedding_response, normalize_text_list


def embed_batch(texts):
    client = get_embeddings_client()
    response = client.embeddings.create(model=default_embedding_model(), input=normalize_text_list(texts))
    return batch_embedding_response(response)
