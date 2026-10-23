from azure.cosmos import CosmosClient

from database_client import load_config


def record_text_safety(payload, config=None):
    cfg = load_config(config)
    with CosmosClient(cfg['endpoint'], credential=cfg['api_key']) as client:
        container = client.get_database_client(cfg['database']).get_container_client(cfg['container'])
        item = container.read_item(item=payload['id'], partition_key=payload.get('partition_key', payload['id']))
    text = ' '.join(str(item.get(field, '')) for field in payload.get('fields') or ['text', 'content', 'message'])
    unsafe = any(token in text.lower() for token in payload.get('blocked_terms') or ['hate', 'violence', 'self-harm'])
    return {'safe': not unsafe, 'id': item.get('id')}
