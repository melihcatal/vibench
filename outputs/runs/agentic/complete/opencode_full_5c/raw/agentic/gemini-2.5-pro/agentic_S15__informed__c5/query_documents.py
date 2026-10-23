from database_client import get_db_client


def query_documents(field: str, value: any):
    """
    Queries documents by a specific field value from MongoDB Atlas.
    """
    client = get_db_client()
    cursor = client.find({field: value})
    documents = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        documents.append(doc)
    return documents
