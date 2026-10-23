import os
from database_client import get_mongo_client, get_database, get_collection
from database_models import normalize_document


def upsert_document(
    collection_name: str, document: dict, id_field: str = "_id"
) -> dict:
    """
    Upserts a JSON document into a specified MongoDB collection by its primary identifier.
    """
    client = get_mongo_client()
    database = get_database(client)
    collection = get_collection(database, collection_name)

    normalized_doc = normalize_document(document)
    document_id = normalized_doc.get(id_field)

    if not document_id:
        raise ValueError(
            f"Document must contain an '{id_field}' field for upsert operation."
        )

    result = collection.update_one(
        {id_field: document_id}, {"$set": normalized_doc}, upsert=True
    )
    client.close()
    return {
        "matched_count": result.matched_count,
        "modified_count": result.modified_count,
        "upserted_id": str(result.upserted_id) if result.upserted_id else None,
    }
