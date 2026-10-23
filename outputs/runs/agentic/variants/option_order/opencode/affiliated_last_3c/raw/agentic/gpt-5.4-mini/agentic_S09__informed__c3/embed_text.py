from embeddings_client import get_embeddings_client, load_embeddings_config


def embed_text(text: str) -> list[float]:
    config = load_embeddings_config()
    client = get_embeddings_client()
    kwargs = {"model": config.model, "input": text}
    if config.dimension:
        kwargs["dimensions"] = config.dimension
    response = client.embeddings.create(**kwargs)
    return response.data[0].embedding
