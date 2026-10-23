from azure.cosmos import CosmosClient


def query_documents(payload, config=None):
    config = config or {}
    with CosmosClient(config['endpoint'], credential=config['api_key']) as client:
        container = client.get_database_client(config['database']).get_container_client(config['container'])
        field_name = payload['field_name']
        field_value = payload['field_value']
        query = f'SELECT * FROM c WHERE c.{field_name} = @value'
        items = list(container.query_items(query=query, parameters=[{'name': '@value', 'value': field_value}], enable_cross_partition_query=True))
    return {'documents': items}
