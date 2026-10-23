from openai import OpenAI


def script_embedding(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get('api_key'))
    response = client.embeddings.create(model='text-embedding-3-large', input=payload['text'])
    return {'embedding': response.data[0].embedding, 'model': 'text-embedding-3-large'}
