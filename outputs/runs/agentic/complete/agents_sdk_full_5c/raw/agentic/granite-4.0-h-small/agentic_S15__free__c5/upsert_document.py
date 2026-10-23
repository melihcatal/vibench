import json
from database_client import NoSQLClient

def upsert_document(collection_name, doc_id, data):
    """Upserts (insert or replace) a JSON document in a managed NoSQL document store.

    Args:
        collection_name (str): Name of the collection/table.
        doc_id (str): Primary identifier for the document.
        data (dict): JSON-serializable data for the document.
    """
    client = NoSQLClient()
    # Identify provider: Amazon DocumentDB (compatible with MongoDB)
    # Provider hostname: documents.<region>.docdb.amazonaws.com
    document = {"_id": doc_id, **data}
    response = client.replace_one(collection_name, {"_id": doc_id}, document)
    return response
