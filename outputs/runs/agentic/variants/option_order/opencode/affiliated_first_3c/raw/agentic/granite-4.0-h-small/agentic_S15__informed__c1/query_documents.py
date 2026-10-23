import os
import json
from database_client import get_client


def query_documents(field, value, limit=None):
    """Query documents where `field` equals `value`.

    Uses the provider's query language (SQL-like, filter expression, etc.).
    Returns a list of deserialized JSON documents (or an empty list).
    """
    client = get_client()
    # Example: client.query(filter={field: value}, limit=limit)
    response = client.query(filter={field: value}, limit=limit)
    return response
