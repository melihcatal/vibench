from embeddings_client import get_client, load_config


def embed_batch(texts: list[str]) -> list[list[float]]:
    client = get_client()
    config = load_config()
    response = client.embed(
        texts=texts, model=config.model, input_type="search_document"
    )
    return response.embeddings
