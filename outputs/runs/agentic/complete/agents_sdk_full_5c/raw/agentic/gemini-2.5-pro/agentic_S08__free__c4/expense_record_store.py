# expense_record_store.py
from document_client import get_mongo_atlas_client
from document_models import NormalizedExpense
from dataclasses import asdict

def save_expense_record(expense: NormalizedExpense, db_name: str, collection_name: str):
    """
    Persists a normalized expense record in a MongoDB Atlas document store.
    
    Args:
        expense: The normalized expense record to save.
        db_name: The name of the database.
        collection_name: The name of the collection.
        
    Returns:
        The ID of the inserted document.
    """
    client = get_mongo_atlas_client()
    db = client[db_name]
    collection = db[collection_name]
    
    expense_dict = asdict(expense)
    
    # Ensure the document has a unique hash to prevent duplicates
    # This assumes source_document_hash is a reliable unique identifier
    result = collection.update_one(
        {"source_document_hash": expense.source_document_hash},
        {"$set": expense_dict},
        upsert=True
    )
    
    if result.upserted_id:
        return result.upserted_id
    else:
        # If the document was updated, we find it to return its ID
        updated_doc = collection.find_one({"source_document_hash": expense.source_document_hash})
        return updated_doc['_id'] if updated_doc else None
