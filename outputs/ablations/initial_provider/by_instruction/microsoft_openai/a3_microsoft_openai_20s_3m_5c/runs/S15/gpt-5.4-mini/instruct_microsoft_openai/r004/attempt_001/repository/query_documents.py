from azure.cosmos import CosmosClient

from database_client import get_database_endpoint, get_database_key, get_database_name, get_container_name
from database_models import normalize_query_value


def query_documents(field_name: str, field_value):
    client = CosmosClient(get_database_endpoint(), credential=get_database_key())
    container = client.get_database_client(get_database_name()).get_container_client(get_container_name())
    value = normalize_query_value(field_value)
    query = f'SELECT * FROM c WHERE c.{field_name} = @value'
    return list(container.query_items(query=query, parameters=[{"name": "@value", "value": value}], enable_cross_partition_query=True))
