from embeddings_client import EmbeddingsClient

client = EmbeddingsClient()


def embed_for_search(
    query: str, documents: list[str]
) -> tuple[list[float], list[list[float]]]:
    query_embedding = client.generate_embedding(query)
    document_embeddings = client.generate_embeddings(documents)
    return query_embedding, document_embeddings
