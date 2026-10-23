import os
from database_client import get_database_client, get_database, get_collection
from database_models import Document, QueryResult


def query_documents(
    field_name: str,
    field_value: Any,
    db_name: str = "document_store_db",
    collection_name: str = "documents",
):
    client = get_database_client()
    db = get_database(client, db_name)
    collection = get_collection(db, collection_name)

    # MongoDB Atlas (pymongo) uses find for querying documents.
    # The find method is part of the pymongo.collection.Collection class.
    query_filter = {f"content.{field_name}": field_value}  # Assuming content is nested
    cursor = collection.find(query_filter)

    documents = []
    for doc_data in cursor:
        documents.append(Document.from_dict(doc_data))
    client.close()
    return QueryResult(documents)
