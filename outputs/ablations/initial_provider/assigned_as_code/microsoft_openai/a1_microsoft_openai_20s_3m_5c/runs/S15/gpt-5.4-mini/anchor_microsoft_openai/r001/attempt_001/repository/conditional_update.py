from azure.cosmos import CosmosClient


def conditional_update(payload, config=None):
    config = config or {}
    with CosmosClient(config['endpoint'], credential=config['api_key']) as client:
        container = client.get_database_client(config['database']).get_container_client(config['container'])
        current = container.read_item(item=payload['id'], partition_key=payload.get('partition_key', payload['id']))
        if payload.get('etag') and current.get('_etag') != payload['etag']:
            return {'updated': False, 'document': current}
        updated = dict(current)
        updated.update(payload.get('updates', {}))
        container.replace_item(item=payload['id'], body=updated)
    return {'updated': True, 'id': payload['id']}
