from embeddings_client import embed_texts


def embed_for_search(query: str, documents):
    vectors = embed_texts([query, *list(documents)])
    return {"query_embedding": vectors[0], "document_embeddings": vectors[1:]}
