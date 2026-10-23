from azure.cosmos import CosmosClient


def conditional_update(id, updates, etag, config=None):
    config = config or {}
    with CosmosClient(config['endpoint'], credential=config['api_key']) as client:
        container = client.get_database_client(config['database']).get_container_client(config['container'])
        document = container.read_item(id, partition_key=id)
        if document['_etag']!= etag:
            raise ValueError('Document has been modified since last read.')
        document.update(updates)
        container.replace_item(id, document)
    return document