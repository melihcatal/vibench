from embeddings_client import get_client


def embed_batch(payload, config=None):
    client, cfg = get_client(config)
    response = client.embeddings.create(model=cfg['model'], input=payload['texts'])
    return {'embeddings': [item.embedding for item in response.data]}
