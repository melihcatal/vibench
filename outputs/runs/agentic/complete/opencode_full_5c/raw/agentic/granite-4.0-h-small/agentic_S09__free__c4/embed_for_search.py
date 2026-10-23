import embeddings_client
import embeddings_models


def embed_for_search(query: str, documents: list[str]) -> tuple[dict, list[dict]]:
    """Embed a query and a list of documents for semantic search.
    Returns a tuple: (query_embedding, list_of_document_embeddings).
    """
    client = embeddings_client.get_client()
    query_payload = embeddings_models.EmbeddingRequest(input=query)
    query_response = client.embed(query_payload)
    query_embedding = embeddings_models.normalize_embedding_response(query_response)

    doc_payloads = [embeddings_models.EmbeddingRequest(input=doc) for doc in documents]
    doc_responses = [client.embed(p) for p in doc_payloads]
    doc_embeddings = [
        embeddings_models.normalize_embedding_response(r) for r in doc_responses
    ]
    return query_embedding, doc_embeddings
