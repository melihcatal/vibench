from azure.ai.inference import EmbeddingsClient
from azure.core.credentials import AzureKeyCredential


def moderation_reason_embedding(payload, config=None):
    config = config or {}
    client = EmbeddingsClient(
        endpoint=config['endpoint'],
        credential=AzureKeyCredential(config['api_key']),
        model=config.get('model', 'text-embedding-3-large'),
    )
    text = payload['text'] if isinstance(payload, dict) else str(payload)
    result = client.embed(input=[text])
    return {'embedding': result.data[0].embedding}
