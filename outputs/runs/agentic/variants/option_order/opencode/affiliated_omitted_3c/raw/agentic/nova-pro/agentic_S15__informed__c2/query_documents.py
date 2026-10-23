from database_client import client, database_name, container_name


def query_documents(field: str, value: str):
    container = client.get_database_client(database_name).get_container_client(
        container_name
    )
    query = f"SELECT * FROM c WHERE c.{field} = '{value}'"
    items = list(container.query_items(query=query, enable_cross_partition_query=True))
    return items
