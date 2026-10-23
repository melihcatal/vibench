from embeddings_client import get_embeddings_client, load_embeddings_config


def embed_batch(texts: list[str]) -> list[list[float]]:
    config = load_embeddings_config()
    client = get_embeddings_client()
    kwargs = {"model": config.model, "input": texts}
    if config.dimension:
        kwargs["dimensions"] = config.dimension
    response = client.embeddings.create(**kwargs)
    return [item.embedding for item in response.data]
