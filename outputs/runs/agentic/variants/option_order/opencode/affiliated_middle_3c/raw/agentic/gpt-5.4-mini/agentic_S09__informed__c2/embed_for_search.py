from embeddings_client import embed_texts


def main(query: str, documents: list[str]) -> dict[str, object]:
    query_embedding = embed_texts([query]).embeddings[0]
    document_embeddings = embed_texts(documents).embeddings
    return {
        "query_embedding": query_embedding,
        "document_embeddings": document_embeddings,
    }
