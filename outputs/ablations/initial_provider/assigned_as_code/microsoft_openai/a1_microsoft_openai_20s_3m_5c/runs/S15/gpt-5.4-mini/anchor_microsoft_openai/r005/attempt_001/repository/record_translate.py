from azure.cosmos import CosmosClient
from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential

from database_client import load_config


def record_translate(payload, config=None):
    cfg = load_config(config)
    translation_client = TextTranslationClient(endpoint=payload['translation_endpoint'], credential=AzureKeyCredential(payload['translation_key']))
    with CosmosClient(cfg['endpoint'], credential=cfg['api_key']) as client:
        container = client.get_database_client(cfg['database']).get_container_client(cfg['container'])
        item = container.read_item(item=payload['id'], partition_key=payload.get('partition_key', payload['id']))
    text = ' '.join(str(item.get(field, '')) for field in payload.get('fields') or ['title', 'summary', 'content'])
    result = translation_client.translate(content=[text], to=[payload['target_language']])
    return {'id': item.get('id'), 'translation': result[0].translations[0].text if result else ''}
