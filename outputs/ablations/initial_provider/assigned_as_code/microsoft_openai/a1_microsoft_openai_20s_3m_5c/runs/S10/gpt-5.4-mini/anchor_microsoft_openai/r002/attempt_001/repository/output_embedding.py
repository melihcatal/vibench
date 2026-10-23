from openai import OpenAI
from model_client import get_config


def output_embedding(payload, config=None):
    resolved = get_config(config)
    text = payload.get('text') or ''
    with OpenAI(api_key=resolved['api_key']) as client:
        response = client.embeddings.create(model='text-embedding-3-large', input=text)
    return {'embedding': response.data[0].embedding}
