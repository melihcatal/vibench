from embeddings_client import get_cohere_client


def embed_for_search(query: str, documents: list[str]):
    cohere_client = get_cohere_client()

    query_embedding = cohere_client.embed(
        texts=[query], model="embed-english-v3.0", input_type="search_query"
    ).embeddings[0]

    document_embeddings = cohere_client.embed(
        texts=documents, model="embed-english-v3.0", input_type="search_document"
    ).embeddings

    return {
        "query_embedding": query_embedding,
        "document_embeddings": document_embeddings,
    }
