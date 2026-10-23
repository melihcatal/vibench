from database_client import get_database_and_container
from typing import Dict, Any

def query_documents(query: str, parameters: list[Dict[str, Any]] = None):
    _, container = get_database_and_container()
    items = list(container.query_items(
        query=query,
        parameters=parameters,
        enable_cross_partition_query=True
    ))
    return items
