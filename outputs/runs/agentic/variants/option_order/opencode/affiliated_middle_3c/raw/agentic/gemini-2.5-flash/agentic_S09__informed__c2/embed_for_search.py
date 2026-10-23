from embeddings_client import EmbeddingsClient


def embed_for_search(query: str, documents: list[str]) -> dict:
    """
    Embeds a query and a list of documents for semantic search.
    Returns a dictionary containing the query embedding and document embeddings.
    """
    client = EmbeddingsClient()
    all_texts = [query] + documents
    embeddings = client.embed_batch(all_texts)

    query_embedding = embeddings[0]
    document_embeddings = embeddings[1:]

    return {
        "query_embedding": query_embedding,
        "document_embeddings": document_embeddings,
    }


if __name__ == "__main__":
    search_query = "animals in the wild"
    search_documents = [
        "A group of lions hunting in the savanna.",
        "Domestic cats enjoy napping in sunbeams.",
        "The Amazon rainforest is home to many exotic species.",
    ]

    search_results = embed_for_search(search_query, search_documents)
    print(
        f"Query embedding (first 5 elements): {search_results['''query_embedding'''][:5]}..."
    )
    print(
        f"Number of document embeddings: {len(search_results['''document_embeddings'''])}"
    )
    for i, doc_emb in enumerate(search_results["""document_embeddings"""]):
        print(f"Document {i + 1} embedding (first 5 elements): {doc_emb[:5]}...")
