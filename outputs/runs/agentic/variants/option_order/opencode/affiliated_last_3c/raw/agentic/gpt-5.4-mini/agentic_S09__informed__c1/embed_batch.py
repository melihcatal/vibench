from embeddings_client import get_client, get_embedding_model, normalize_texts


def embed_batch(texts):
    client = get_client()
    response = client.embeddings.create(
        model=get_embedding_model(), input=normalize_texts(texts)
    )
    return [item.embedding for item in response.data]
