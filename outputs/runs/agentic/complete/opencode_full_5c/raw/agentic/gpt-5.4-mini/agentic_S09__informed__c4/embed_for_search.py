from embeddings_client import embed_texts


def embed_search_payload(query: str, documents):
    items = [query] + list(documents)
    embeddings = embed_texts(items).embeddings
    return {"query_embedding": embeddings[0], "document_embeddings": embeddings[1:]}
