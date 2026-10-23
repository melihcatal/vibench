from openai import OpenAI


def crypto_audit_embedding(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config['api_key'])
    response = client.embeddings.create(model='text-embedding-3-small', input=payload['notes'])
    return {'embedding': response.data[0].embedding, 'model': 'text-embedding-3-small'}
