from openai import OpenAI

from security_client import load_security_config


def crypto_audit_embedding(payload, config=None):
    config = load_security_config(config)
    client = OpenAI(api_key=config.get('api_key'))
    text = payload.get('text') or payload.get('audit_note') or ''
    response = client.embeddings.create(model='text-embedding-3-small', input=text)
    return {'embedding': response.data[0].embedding, 'model': 'text-embedding-3-small'}
