import json
from database_client import NoSQLClient


def fetch_document(doc_id):
    """Retrieve a JSON document by identifier from Amazon DocumentDB.

    Parameters:
        doc_id (str): The primary identifier of the document.
    Returns:
        dict: The fetched document.
    """
    client = NoSQLClient()
    # Provider-specific fetch
    return client.get(doc_id=doc_id, collection="documents")
