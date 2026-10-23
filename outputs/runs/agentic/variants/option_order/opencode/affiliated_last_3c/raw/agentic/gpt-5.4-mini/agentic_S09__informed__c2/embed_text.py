from embeddings_client import create_client, get_model_name


def embed_text(text: str):
    client = create_client()
    response = client.embeddings.create(model=get_model_name(), input=text)
    return response.data[0].embedding
