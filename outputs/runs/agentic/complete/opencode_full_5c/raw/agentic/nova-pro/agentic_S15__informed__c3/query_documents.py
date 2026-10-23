from database_client import client, database, container
from database_models import parse_response


def query_documents(field_name: str, field_value: str):
    query = f'SELECT * FROM c WHERE c.{field_name} = "{field_value}"'
    items = list(container.query_items(query=query, enable_cross_partition_query=True))
    return [parse_response(item) for item in items]
