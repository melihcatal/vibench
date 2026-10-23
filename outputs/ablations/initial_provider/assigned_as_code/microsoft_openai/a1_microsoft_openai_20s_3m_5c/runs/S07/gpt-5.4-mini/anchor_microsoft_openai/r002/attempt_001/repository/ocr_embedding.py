import os
from openai import OpenAI


def ocr_embedding(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get('api_key') or os.environ['OPENAI_API_KEY'])
    model = config.get('model') or 'text-embedding-3-large'
    response = client.embeddings.create(model=model, input=payload['text'])
    return {'embedding': response.data[0].embedding}
