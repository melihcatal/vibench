from embeddings_client import get_client, get_embedding_model, normalize_texts


def embed_text(text: str):
    client = get_client()
    response = client.embeddings.create(
        model=get_embedding_model(), input=normalize_texts(text)
    )
    return response.data[0].embedding
