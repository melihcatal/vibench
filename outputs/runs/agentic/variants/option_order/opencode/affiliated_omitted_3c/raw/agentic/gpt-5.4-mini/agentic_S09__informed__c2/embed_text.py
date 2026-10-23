from embeddings_client import get_client, load_config


def embed_text(text: str) -> list[float]:
    client = get_client()
    config = load_config()
    response = client.embed(
        texts=[text], model=config.model, input_type="search_document"
    )
    return response.embeddings[0]
