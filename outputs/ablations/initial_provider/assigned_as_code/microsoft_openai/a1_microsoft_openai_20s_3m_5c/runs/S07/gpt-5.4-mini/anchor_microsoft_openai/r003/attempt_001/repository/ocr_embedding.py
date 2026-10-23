import os
from openai import OpenAI


def ocr_embedding(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get('api_key') or os.environ['OPENAI_API_KEY'])
    model = config.get('model', 'text-embedding-3-large')
    texts = payload.get('sections') or [payload['text']]
    response = client.embeddings.create(model=model, input=texts)
    return {'embeddings': [item.embedding for item in response.data]}
