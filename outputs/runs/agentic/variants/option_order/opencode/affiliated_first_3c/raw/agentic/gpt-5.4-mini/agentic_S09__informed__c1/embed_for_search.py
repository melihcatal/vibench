from embed_text import embed_text


def embed_for_search(query, documents):
    query_embedding = embed_text(query)
    document_embeddings = [(doc, embed_text(doc)) for doc in documents]
    return {
        "query_embedding": query_embedding,
        "document_embeddings": document_embeddings,
    }
