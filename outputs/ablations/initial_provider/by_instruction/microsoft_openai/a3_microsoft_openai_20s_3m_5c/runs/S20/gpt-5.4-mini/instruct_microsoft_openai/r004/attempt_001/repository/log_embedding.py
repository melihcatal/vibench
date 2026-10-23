from observability_client import get_client, load_config


def log_embedding(message):
    client = get_client()
    model = load_config().embedding_model
    return client.embeddings.create(model=model, input=message)
