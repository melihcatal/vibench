from azure.cosmos import CosmosClient

from database_client import load_config


def record_summary(payload, config=None):
    cfg = load_config(config)
    with CosmosClient(cfg['endpoint'], credential=cfg['api_key']) as client:
        container = client.get_database_client(cfg['database']).get_container_client(cfg['container'])
        item = container.read_item(item=payload['id'], partition_key=payload.get('partition_key', payload['id']))
    fields = payload.get('fields') or ['title', 'name', 'summary']
    summary = {field: item.get(field) for field in fields if field in item}
    return {'summary': summary, 'id': item.get('id')}
