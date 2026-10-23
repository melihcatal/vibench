from database_client import get_container_client


def query_documents(database_name, container_name, query_string, parameters=None):
    container = get_container_client(database_name, container_name)
    results = list(container.query_items(
        query=query_string,
        parameters=parameters or [],
        enable_cross_partition_query=True  # Enable if querying across partitions
    ))
    return results
