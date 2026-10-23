import embeddings_client

def embed_for_search(query, documents, config=None):
    client = embeddings_client.get_client(config)
    query_embedding = embeddings_client.embed_text({'text': query}, config)
    document_embeddings = [embeddings_client.embed_text({'text': doc}, config) for doc in documents]
    return {'query_embedding': query_embedding, 'document_embeddings': document_embeddings}