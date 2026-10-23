import json
from database_client import NoSQLClient


def query_documents(field, value):
    """Query documents by a field value or partition-style key in DocumentDB.

    Parameters:
        field (str): Field name to filter on.
        value: Value to match for the given field.
    Returns:
        list[dict]: Matching documents.
    """
    client = NoSQLClient()
    # Provider-specific query
    return client.query(filter={field: value}, collection="documents")
