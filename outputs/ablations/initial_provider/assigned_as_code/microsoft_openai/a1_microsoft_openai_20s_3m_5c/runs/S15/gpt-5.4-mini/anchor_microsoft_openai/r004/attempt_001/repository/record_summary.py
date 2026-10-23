from azure.cosmos import CosmosClient


def record_summary(payload, config=None):
    config = config or {}
    with CosmosClient(config['endpoint'], credential=config['api_key']) as client:
        container = client.get_database_client(config['database']).get_container_client(config['container'])
        item = container.read_item(item=payload['id'], partition_key=payload.get('partition_key', payload['id']))
    return {'id': item['id'], 'summary': item.get('summary') or item.get('title') or ''}
