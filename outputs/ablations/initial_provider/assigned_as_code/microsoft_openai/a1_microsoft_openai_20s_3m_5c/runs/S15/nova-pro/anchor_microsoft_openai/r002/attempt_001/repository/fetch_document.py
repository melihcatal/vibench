from azure.cosmos import CosmosClient


def fetch_document(id, config=None):
    config = config or {}
    with CosmosClient(config['endpoint'], credential=config['api_key']) as client:
        container = client.get_database_client(config['database']).get_container_client(config['container'])
        document = container.read_item(id, partition_key=id)
    return document