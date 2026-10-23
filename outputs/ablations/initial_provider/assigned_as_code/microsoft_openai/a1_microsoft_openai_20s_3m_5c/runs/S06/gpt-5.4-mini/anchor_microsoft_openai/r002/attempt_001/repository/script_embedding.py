from openai import OpenAI


def script_embedding(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get('api_key'))
    response = client.embeddings.create(model=config.get('model', 'text-embedding-3-small'), input=payload['text'])
    return {'embedding': response.data[0].embedding, 'model': response.model}
