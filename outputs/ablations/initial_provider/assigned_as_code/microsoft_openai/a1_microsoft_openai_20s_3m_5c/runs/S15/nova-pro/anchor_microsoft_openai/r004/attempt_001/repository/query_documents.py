from azure.cosmos import CosmosClient

from database_client import get_cosmos_client


def query_documents(field, value, config=None):
    client = get_cosmos_client(config)
    container = client.get_database_client(config['database']).get_container_client(config['container'])
    query = f'SELECT * FROM c WHERE c.{field} = "{value}"'
    documents = list(container.query_items(query=query, enable_cross_partition_query=True))
    return documents