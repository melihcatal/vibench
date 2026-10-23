from embeddings_client import get_client


def embed_for_search(payload, config=None):
    client, cfg = get_client(config)
    texts = [payload['query']] + payload['documents']
    response = client.embeddings.create(model=cfg['model'], input=texts)
    embeddings = [item.embedding for item in response.data]
    return {'query_embedding': embeddings[0], 'document_embeddings': embeddings[1:]}
