from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from typing import Dict, Any

from document_client import get_mongo_connection_string
from document_models import NormalizedExpense

def expense_record_store(
    expense_data: NormalizedExpense,
    db_name: str,
    collection_name: str
) -> str:
    """
    Persists a normalized expense record in a MongoDB Atlas collection.
    """
    connection_string = get_mongo_connection_string()
    if not connection_string:
        raise ValueError("MONGO_ATLAS_CONNECTION_STRING is not set.")

    client = MongoClient(connection_string)

    try:
        # The ismaster command is cheap and does not require auth.
        client.admin.command('ismaster')
    except ConnectionFailure:
        raise ConnectionFailure("MongoDB Atlas server not available.")

    db = client[db_name]
    collection = db[collection_name]
    
    # Convert Pydantic model to dict for insertion
    expense_dict = expense_data.model_dump()

    result = collection.insert_one(expense_dict)
    
    return str(result.inserted_id)
