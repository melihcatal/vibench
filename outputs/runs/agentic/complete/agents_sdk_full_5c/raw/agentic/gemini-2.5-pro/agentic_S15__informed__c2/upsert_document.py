from pymongo.results import UpdateResult
from database_client import get_db_collection
from database_models import Document

def upsert_document(document: Document) -> UpdateResult:
    """
    Upserts a document in the MongoDB Atlas collection.

    If a document with the same _id exists, it will be replaced.
    Otherwise, a new document will be inserted.

    Args:
        document: The Document object to upsert.

    Returns:
        The result of the replace_one operation.
    """
    collection = get_db_collection()
    document_dict = document.to_dict()
    
    # Using MongoDB's replace_one with upsert=True is a common way to handle "upsert"
    result = collection.replace_one(
        {"_id": document.doc_id},
        document_dict,
        upsert=True
    )
    
    print(f"Upserted document with ID: {document.doc_id}. Matched: {result.matched_count}, Modified: {result.modified_count}, Upserted ID: {result.upserted_id}")
    return result
