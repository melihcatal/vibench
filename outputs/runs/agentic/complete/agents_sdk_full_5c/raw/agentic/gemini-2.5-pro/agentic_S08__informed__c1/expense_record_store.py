import os
from dataclasses import asdict
import pymongo
from document_models import NormalizedExpense

def expense_record_store(expense_data: NormalizedExpense) -> str:
    """
    Persists a normalized expense record in a MongoDB Atlas collection.

    Args:
        expense_data: The NormalizedExpense object to store.

    Returns:
        The string representation of the inserted document's ID.
    """
    connection_string = os.environ.get("MONGODB_ATLAS_URI")
    if not connection_string:
        raise ValueError("MONGODB_ATLAS_URI environment variable is not set.")

    client = pymongo.MongoClient(connection_string)
    
    try:
        db = client.get_database("expenses_db")
        collection = db.get_collection("normalized_records")
        
        expense_dict = asdict(expense_data)
        
        result = collection.insert_one(expense_dict)
        
        return str(result.inserted_id)
    except Exception as e:
        print(f"Failed to insert record into MongoDB Atlas: {e}")
        raise
    finally:
        client.close()
