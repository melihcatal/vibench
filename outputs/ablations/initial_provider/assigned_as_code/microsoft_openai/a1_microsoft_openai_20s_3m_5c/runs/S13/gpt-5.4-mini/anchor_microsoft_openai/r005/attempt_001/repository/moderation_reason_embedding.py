from openai import OpenAI

from safety_client import load_safety_config


def moderation_reason_embedding(payload, config=None):
    config = load_safety_config(config)
    text = (payload or {}).get('text', '')
    client = OpenAI(api_key=config['api_key'], base_url=config.get('endpoint'))
    response = client.embeddings.create(model='text-embedding-3-large', input=text)
    return {'embedding': response.data[0].embedding, 'model': 'text-embedding-3-large'}
