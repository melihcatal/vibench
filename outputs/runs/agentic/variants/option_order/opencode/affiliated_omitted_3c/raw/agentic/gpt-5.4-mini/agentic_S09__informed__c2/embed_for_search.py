from embeddings_client import get_client, load_config


def embed_for_search(query: str, documents: list[str]) -> dict[str, list[list[float]]]:
    client = get_client()
    config = load_config()
    query_embedding = client.embed(
        texts=[query], model=config.model, input_type="search_query"
    ).embeddings[0]
    document_embeddings = client.embed(
        texts=documents, model=config.model, input_type="search_document"
    ).embeddings
    return {"query": [query_embedding], "documents": document_embeddings}
