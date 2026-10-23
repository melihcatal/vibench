import os
from database_client import get_database_client, get_database, get_collection
from database_models import Document


def upsert_document(
    document_id: str,
    content: dict,
    db_name: str = "document_store_db",
    collection_name: str = "documents",
):
    client = get_database_client()
    db = get_database(client, db_name)
    collection = get_collection(db, collection_name)

    document_data = Document(document_id, content).to_dict()

    # MongoDB Atlas (pymongo) uses update_one with upsert=True for upsert operations.
    # The update_one method is part of the pymongo.collection.Collection class.
    result = collection.update_one({"_id": document_id}, {"$set": content}, upsert=True)
    client.close()
    return {
        "document_id": document_id,
        "upserted_id": str(result.upserted_id) if result.upserted_id else None,
        "matched_count": result.matched_count,
        "modified_count": result.modified_count,
    }
