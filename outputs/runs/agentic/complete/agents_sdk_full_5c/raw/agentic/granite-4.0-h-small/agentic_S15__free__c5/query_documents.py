def query_documents(collection_name, query):
    """Queries documents using a field value or partition-style key.

    Args:
        collection_name (str): Name of the collection/table.
        query (dict): Query expression where each key is a field and value is a match value or range.

    Returns:
        list: List of documents that match the query.
    """  
    from database_client import NoSQLClient
    client = NoSQLClient()
    # Provider: Amazon DocumentDB
    return client.find(collection_name, query)
