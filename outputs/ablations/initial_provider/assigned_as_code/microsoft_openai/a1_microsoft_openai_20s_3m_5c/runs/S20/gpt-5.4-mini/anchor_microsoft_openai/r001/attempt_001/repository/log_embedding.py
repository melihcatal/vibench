from observability_client import inference_clients, load_config


def log_embedding(payload, config=None):
    cfg = load_config(config)
    clients = inference_clients(cfg)
    texts = payload['texts']
    response = clients['embeddings'].embed(input=texts, model=cfg.get('embedding_model', 'text-embedding-3-small'))
    return {'embeddings': [item.embedding for item in response.data]}
