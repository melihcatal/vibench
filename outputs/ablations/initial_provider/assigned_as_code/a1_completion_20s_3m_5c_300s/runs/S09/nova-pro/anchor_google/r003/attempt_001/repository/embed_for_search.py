from embeddings_client import DirectEmbeddingsClient


def embed_for_search(query, documents, config=None):
    client = DirectEmbeddingsClient(config)
    query_embedding = client.embed_text({"text": query})
    document_embeddings = [client.embed_text({"text": doc}) for doc in documents]
    scores = client.calculate_similarities(query_embedding, document_embeddings)
    return {"query_embedding": query_embedding, "document_embeddings": document_embeddings, "scores": scores}