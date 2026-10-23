from embeddings_client import get_client, get_model


def embed_for_search(payload, config=None):
    config = config or {}
    query = payload['query']
    documents = payload['documents']
    with get_client(config) as client:
        query_embedding = client.embeddings.create(model=get_model(config), input=query).data[0].embedding
        doc_embeddings = client.embeddings.create(model=get_model(config), input=documents).data
    return {'query_embedding': query_embedding, 'document_embeddings': [item.embedding for item in doc_embeddings]}
