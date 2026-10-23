import os
from database_client import get_database_client, get_database, get_collection
from database_models import Document


def fetch_document(
    document_id: str,
    db_name: str = "document_store_db",
    collection_name: str = "documents",
):
    client = get_database_client()
    db = get_database(client, db_name)
    collection = get_collection(db, collection_name)

    # MongoDB Atlas (pymongo) uses find_one to fetch a single document by its _id.
    # The find_one method is part of the pymongo.collection.Collection class.
    document_data = collection.find_one({"_id": document_id})
    client.close()

    if document_data:
        # Ensure the content is directly accessible, not nested under a 'content' key if that's how it was stored
        # If the original upsert stored it as {"_id": document_id, "content": content}, then this is correct.
        return Document.from_dict(document_data)
    return None
