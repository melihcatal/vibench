import os
from openai import OpenAI

def embed_output(payload, config=None):
    config = config or {}
    with OpenAI(api_key=config.get('api_key') or os.environ['OPENAI_API_KEY']) as client:
        response = client.embeddings.create(model='gpt-5.4-mini',
            input=payload['text'])
    return {'embedding': response.data[0].embedding}
