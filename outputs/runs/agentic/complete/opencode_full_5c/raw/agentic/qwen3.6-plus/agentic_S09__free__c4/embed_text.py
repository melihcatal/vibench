from embeddings_client import (
    get_openai_client,
    create_embedding_payload,
    extract_embeddings,
    handle_openai_error,
    DEFAULT_EMBEDDING_MODEL,
)


def embed_text(text: str, model: str = DEFAULT_EMBEDDING_MODEL, dimensions: int = None):
    client = get_openai_client()
    payload = create_embedding_payload([text], model=model, dimensions=dimensions)
    try:
        response = client.embeddings.create(**payload)
        embeddings = extract_embeddings(response)
        return embeddings[0]
    except Exception as exc:
        handle_openai_error(exc)
