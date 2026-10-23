from openai import AzureOpenAI

from storage_models import build_metadata_document


def asset_metadata_embedding(payload, config=None):
    config = config or {}
    client = AzureOpenAI(azure_endpoint=config['openai_endpoint'], api_key=config['openai_key'], api_version=config.get('openai_api_version', '2024-06-01'))
    document = build_metadata_document(payload['object_name'], payload.get('metadata'), payload.get('text'))
    text = f"{document['object_name']}\n{document['metadata']}\n{document['text']}"
    response = client.embeddings.create(model=config['embedding_model'], input=text)
    return {'embedding': response.data[0].embedding, 'document': document}
