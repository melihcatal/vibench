import os
from database_client import ManagedNoSQLClient


def query_documents(field, value):
    """Query documents in the NoSQL store where `field` matches `value`.

    Args:
        field (str): Document field to filter on.
        value: Value to match (can be exact match or prefix depending on provider).

    Returns:
        list: List of matching documents (empty if none).
    """
    client = ManagedNoSQLClient()
    # Provider-specific query (e.g., scan, filter_expression, or where clause)
    results = client.scan(field=field, value=value)
    print(f"Queried {len(results)} documents for {field}={value}.")
    return results
