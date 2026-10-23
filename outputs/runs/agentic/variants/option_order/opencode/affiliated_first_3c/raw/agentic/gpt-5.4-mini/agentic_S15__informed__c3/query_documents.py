from database_client import get_container
from database_models import make_query_value


def query_documents(field_name, field_value):
    container = get_container()
    value = make_query_value(field_value)
    query = f"SELECT * FROM c WHERE c.{field_name} = @value"
    return list(
        container.query_items(
            query=query,
            parameters=[{"name": "@value", "value": value}],
            enable_cross_partition_query=True,
        )
    )
