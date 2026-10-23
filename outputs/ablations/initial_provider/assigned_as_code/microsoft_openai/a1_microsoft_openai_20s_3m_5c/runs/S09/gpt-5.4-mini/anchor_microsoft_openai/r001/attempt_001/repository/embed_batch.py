from openai import OpenAI

from embeddings_client import get_api_key, get_embedding_model
from embeddings_models import normalize_texts


def embed_batch(payload, config=None):
    config = config or {}
    texts = normalize_texts(payload['texts'])
    with OpenAI(api_key=get_api_key(config)) as client:
        response = client.embeddings.create(model=get_embedding_model(config), input=texts)
    return {'embeddings': [item.embedding for item in response.data]}
