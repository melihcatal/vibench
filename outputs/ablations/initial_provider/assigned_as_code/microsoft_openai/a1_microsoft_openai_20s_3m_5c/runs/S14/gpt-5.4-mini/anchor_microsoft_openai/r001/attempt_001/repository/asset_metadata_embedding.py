from openai import OpenAI


def asset_metadata_embedding(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config['openai_api_key'])
    text = payload.get('text', '')
    metadata = payload.get('metadata', {})
    response = client.embeddings.create(model='text-embedding-3-small', input=[f'{metadata} {text}'])
    return {'embedding': response.data[0].embedding}
