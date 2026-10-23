from embeddings_client import get_client
from embeddings_models import cosine_similarity


def similarity_score(payload, config=None):
    client, cfg = get_client(config)
    response = client.embeddings.create(model=cfg['model'], input=[payload['text_a'], payload['text_b']])
    embeddings = [item.embedding for item in response.data]
    return {'similarity': cosine_similarity(embeddings[0], embeddings[1])}
