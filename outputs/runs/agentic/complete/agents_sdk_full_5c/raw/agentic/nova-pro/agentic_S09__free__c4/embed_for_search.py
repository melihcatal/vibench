from embeddings_client import EmbeddingsClient

client = EmbeddingsClient()

def embed_for_search(query, documents):
    query_embedding = client.embed_text(query)
    document_embeddings = client.embed_batch(documents)
    return client.search(query_embedding, document_embeddings)