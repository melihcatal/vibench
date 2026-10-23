from azure.cosmos import CosmosClient

from database_client import get_client


def query_documents(query, config=None):
    client = get_client(config)
    container = client.get_database_client(config['database']).get_container_client(config['container'])
    return list(container.query_items(
        query=query,
        enable_cross_partition_query=True
    ))