from azure.cosmos import CosmosClient

def query_documents(field, value, config=None):
    config = config or {}
    with CosmosClient(config['endpoint'], credential=config['api_key']) as client:
        container = client.get_database_client(config['database']).get_container_client(config['container'])
        query = f'SELECT * FROM c WHERE c.{field} = "{value}"'
        documents = list(container.query_items(query=query, enable_cross_partition_query=True))
    return documents