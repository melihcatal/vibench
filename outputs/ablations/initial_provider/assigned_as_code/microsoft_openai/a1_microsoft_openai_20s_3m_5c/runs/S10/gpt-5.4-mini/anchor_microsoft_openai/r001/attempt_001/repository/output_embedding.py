from openai import OpenAI
from model_client import get_api_key, get_model
from model_models import text_from_payload


def output_embedding(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=get_api_key(config))
    response = client.embeddings.create(model=config.get('embedding_model') or 'text-embedding-3-small', input=text_from_payload(payload))
    return {'embedding': response.data[0].embedding}
