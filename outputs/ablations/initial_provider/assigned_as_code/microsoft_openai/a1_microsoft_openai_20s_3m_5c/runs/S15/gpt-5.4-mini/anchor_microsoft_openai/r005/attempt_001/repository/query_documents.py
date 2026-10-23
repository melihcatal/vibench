from azure.cosmos import CosmosClient

from database_client import load_config


def query_documents(payload, config=None):
    cfg = load_config(config)
    with CosmosClient(cfg['endpoint'], credential=cfg['api_key']) as client:
        container = client.get_database_client(cfg['database']).get_container_client(cfg['container'])
        if 'key' in payload:
            query = 'SELECT * FROM c WHERE c.partitionKey = @key'
            params = [{'name': '@key', 'value': payload['key']}]
        else:
            query = f"SELECT * FROM c WHERE c.{payload['field']} = @value"
            params = [{'name': '@value', 'value': payload['value']}]
        items = list(container.query_items(query=query, parameters=params, enable_cross_partition_query=True))
    return {'documents': items}
