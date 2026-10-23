from embeddings_client import create_client, get_model_name


def embed_batch(texts):
    client = create_client()
    response = client.embeddings.create(model=get_model_name(), input=list(texts))
    return [item.embedding for item in response.data]
