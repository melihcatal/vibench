from database_client import get_db_client
from bson import ObjectId


def upsert_document(document_id: str, data: dict):
    """
    Upserts a document in MongoDB Atlas.
    """
    client = get_db_client()
    query = {"_id": ObjectId(document_id)}

    # Check if document exists to handle versioning
    existing_doc = client.find_one(query)

    if existing_doc:
        new_version = existing_doc.get("_version", 1) + 1
        update = {"$set": data, "$set": {"_version": new_version}}
        result = client.update_one(query, update)
    else:
        # Insert new document with version 1
        new_document = {"_id": ObjectId(document_id), **data, "_version": 1}
        result = client.insert_one(new_document)

    return result
