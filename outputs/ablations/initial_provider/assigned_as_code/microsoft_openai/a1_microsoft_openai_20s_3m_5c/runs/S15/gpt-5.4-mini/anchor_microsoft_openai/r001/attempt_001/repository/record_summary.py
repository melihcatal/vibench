from azure.cosmos import CosmosClient


def record_summary(payload, config=None):
    config = config or {}
    with CosmosClient(config['endpoint'], credential=config['api_key']) as client:
        container = client.get_database_client(config['database']).get_container_client(config['container'])
        document = container.read_item(item=payload['id'], partition_key=payload.get('partition_key', payload['id']))
    text = ' '.join(str(v) for v in document.values() if isinstance(v, (str, int, float, bool)))
    return {'summary': text[:280], 'id': payload['id']}
