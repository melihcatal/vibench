from azure.cosmos import CosmosClient

def conditional_update(id, payload, config=None):
    config = config or {}
    with CosmosClient(config['endpoint'], credential=config['api_key']) as client:
        container = client.get_database_client(config['database']).get_container_client(config['container'])
        document = container.read_item(item=id, partition_key=id)
        for key, value in payload.items():
            if key in document:
                document[key] = value
        container.upsert_item(document)
    return document