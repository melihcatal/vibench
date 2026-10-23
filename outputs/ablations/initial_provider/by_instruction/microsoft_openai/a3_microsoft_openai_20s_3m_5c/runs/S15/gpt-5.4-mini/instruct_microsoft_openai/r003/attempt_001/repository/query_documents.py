from database_client import get_container
from database_models import build_response


def query_documents(field_name, field_value):
    container = get_container()
    query = f"SELECT * FROM c WHERE c.{field_name} = @value"
    items = list(container.query_items(query=query, parameters=[{"name": "@value", "value": field_value}], enable_cross_partition_query=True))
    return build_response(items)
