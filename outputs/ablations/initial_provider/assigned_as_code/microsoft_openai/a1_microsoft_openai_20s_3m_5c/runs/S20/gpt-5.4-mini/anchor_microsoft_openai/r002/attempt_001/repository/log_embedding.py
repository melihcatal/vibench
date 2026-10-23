from openai import OpenAI


def log_embedding(payload, config=None):
    client = OpenAI(api_key=config['api_key'])
    response = client.embeddings.create(model=config.get('model', 'text-embedding-3-large'), input=payload['texts'])
    return {'embeddings': [item.embedding for item in response.data]}
