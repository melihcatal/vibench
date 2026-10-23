from model_client import get_client, pick_model


def embed_output(text, model=None):
    client = get_client()
    response = client.embeddings.create(
        model=pick_model(model, family="embedding"), input=text
    )
    return response.data[0].embedding
