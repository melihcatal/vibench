import os
from database_client import ManagedNoSQLClient


def fetch_document(identifier):
    """Retrieve a JSON document from the managed NoSQL store by its primary identifier.

    Args:
        identifier (str): The document's unique key.

    Returns:
        dict: The fetched document, or None if not found.
    """
    client = ManagedNoSQLClient()
    # Provider-specific fetch call (e.g., get by key)
    document = client.get(identifier)
    if document is None:
        print(f"Document {identifier} not found.")
    return document
