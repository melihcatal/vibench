from openai import OpenAI

from model_client import get_client, get_model


def output_embedding(payload, config=None):
    client = get_client(config)
    model = config.get('embedding_model') if config else None
    model = model or 'text-embedding-3-large'
    response = client.embeddings.create(model=model, input=payload['text'])
    return {'embedding': response.data[0].embedding}
