def fetch_document(collection_name, doc_id):
    """Fetches a single document by its primary identifier from a managed NoSQL document store.

    Args:
        collection_name (str): Name of the collection/table.
        doc_id (str): Document primary identifier.

    Returns:
        dict: The fetched document if found, otherwise None.
    """  
    from database_client import NoSQLClient
    client = NoSQLClient()
    # Provider: Amazon DocumentDB (MongoDB compatible)
    # Provider hostname format: documents.<region>.docdb.amazonaws.com
    return client.find_one(collection_name, {"_id": doc_id})
