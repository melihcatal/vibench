from openai import OpenAI

from embeddings_client import get_api_key, get_embedding_model
from embeddings_models import normalize_texts


def embed_for_search(payload, config=None):
    config = config or {}
    query = payload['query']
    documents = normalize_texts(payload['documents'])
    with OpenAI(api_key=get_api_key(config)) as client:
        response = client.embeddings.create(model=get_embedding_model(config), input=[query] + documents)
    embeddings = [item.embedding for item in response.data]
    return {'query_embedding': embeddings[0], 'document_embeddings': embeddings[1:]}
