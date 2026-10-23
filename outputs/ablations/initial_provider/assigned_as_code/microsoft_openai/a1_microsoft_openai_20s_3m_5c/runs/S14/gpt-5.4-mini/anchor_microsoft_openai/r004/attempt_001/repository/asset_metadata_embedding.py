from openai import OpenAI

from storage_client import load_storage_config


def asset_metadata_embedding(payload, config=None):
    resolved = load_storage_config(config)
    client = OpenAI(api_key=resolved['openai_api_key'])
    text = ' '.join(str(payload.get(key, '')) for key in ['object_name', 'content_type', 'text'])
    embedding = client.embeddings.create(model=resolved.get('embedding_model', 'text-embedding-3-large'), input=text)
    return {'embedding': embedding.data[0].embedding}
