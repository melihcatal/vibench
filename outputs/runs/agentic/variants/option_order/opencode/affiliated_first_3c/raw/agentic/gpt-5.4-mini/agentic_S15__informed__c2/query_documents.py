from database_client import get_container, as_dict


def query_documents(
    database_name: str, container_name: str, field_name: str, field_value
):
    container = get_container(database_name, container_name)
    query = f"SELECT * FROM c WHERE c.{field_name} = @value"
    items = list(
        container.query_items(
            query=query,
            parameters=[{"name": "@value", "value": field_value}],
            enable_cross_partition_query=True,
        )
    )
    return [as_dict(item) for item in items]
