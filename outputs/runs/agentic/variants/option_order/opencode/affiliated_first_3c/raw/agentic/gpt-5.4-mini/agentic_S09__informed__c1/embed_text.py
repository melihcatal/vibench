from embeddings_client import get_client, get_embedding_model


def embed_text(text: str):
    client = get_client()
    model = get_embedding_model()
    response = client.embeddings.create(model=model, input=text)
    return response.data[0].embedding
