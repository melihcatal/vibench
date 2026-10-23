from embeddings_client import get_openai_client
from embeddings_models import normalize_text_payload, extract_embeddings_vectors


def embed_batch(payload, config=None):
    client, settings = get_openai_client(config)
    texts = normalize_text_payload(payload)
    response = client.embeddings.create(model=settings['model'], input=texts)
    return {'embeddings': extract_embeddings_vectors(response)}
