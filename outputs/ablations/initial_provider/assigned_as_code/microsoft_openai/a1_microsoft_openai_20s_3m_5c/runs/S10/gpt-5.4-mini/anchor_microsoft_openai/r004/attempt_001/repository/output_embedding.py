from openai import OpenAI


def output_embedding(payload, config=None):
    config = config or {}
    with OpenAI(api_key=config.get('api_key')) as client:
        response = client.embeddings.create(model='text-embedding-3-small', input=payload['text'])
    return {'embedding': response.data[0].embedding}
