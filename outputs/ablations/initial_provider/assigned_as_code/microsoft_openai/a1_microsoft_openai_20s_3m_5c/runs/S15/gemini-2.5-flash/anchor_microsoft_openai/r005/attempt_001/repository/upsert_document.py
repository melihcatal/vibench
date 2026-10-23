from azure.cosmos import CosmosClient


def upsert_document(payload, config=None):
    config = config or {}
    with CosmosClient(config['endpoint'], credential=config['api_key']) as client:
        container = client.get_database_client(config['database']).get_container_client(config['container'])
        document = dict(payload['document'], id=payload['id'])
        container.upsert_item(document)
    return {'id': payload['id']}
