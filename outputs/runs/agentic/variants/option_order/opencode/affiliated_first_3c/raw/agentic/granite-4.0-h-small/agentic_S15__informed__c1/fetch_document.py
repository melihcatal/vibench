import os
from database_client import get_client


def fetch_document(identifier):
    """Fetch a document by its primary identifier from the managed NoSQL store.

    Returns the deserialized JSON document or raises an exception if not found.
    """
    client = get_client()
    # Retrieve operation depends on the concrete provider.
    response = client.get_document(identifier=identifier)
    return response
