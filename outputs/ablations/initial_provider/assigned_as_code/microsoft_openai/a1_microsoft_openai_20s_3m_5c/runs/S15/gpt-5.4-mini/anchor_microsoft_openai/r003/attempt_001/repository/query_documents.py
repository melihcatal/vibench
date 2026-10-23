from database_client import get_container_client, load_config
from database_models import normalize_query_result


def query_documents(payload, config=None):
    config = load_config(config)
    container = get_container_client(config)
    field = payload['field']
    value = payload['value']
    query = f"SELECT * FROM c WHERE c.{field} = @value"
    items = container.query_items(query=query, parameters=[{'name': '@value', 'value': value}], enable_cross_partition_query=True)
    return normalize_query_result(items)
