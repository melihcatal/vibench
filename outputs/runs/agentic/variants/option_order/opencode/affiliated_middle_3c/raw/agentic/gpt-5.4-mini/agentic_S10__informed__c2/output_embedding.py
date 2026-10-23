from model_client import get_embedding_client, select_embedding_model


def embed_output(text: str):
    client = get_embedding_client()
    model = select_embedding_model()
    response = client.embeddings.create(model=model, input=text)
    return response.data[0].embedding
