
import os
import json
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from document_models import NormalizedExpense
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

def get_db_client():
    """Connects to MongoDB Atlas and returns the client."""
    uri = os.environ.get("MONGODB_ATLAS_URI")
    if not uri:
        raise ValueError("MONGODB_ATLAS_URI environment variable not set.")
    
    client = MongoClient(uri)
    # The ismaster command is cheap and does not require auth.
    try:
        client.admin.command('ismaster')
    except ConnectionFailure:
        raise ConnectionFailure("MongoDB Atlas server not available")
    return client

def persist_expense_record(expense_data: NormalizedExpense, db_name: str, collection_name: str) -> str:
    """
    Persists a normalized expense record in a MongoDB Atlas collection.

    Args:
        expense_data: The NormalizedExpense object to store.
        db_name: The name of the database.
        collection_name: The name of the collection.

    Returns:
        The string representation of the inserted document's ID.
    """
    client = get_db_client()
    db = client[db_name]
    collection = db[collection_name]
    
    # Convert Pydantic model to a dictionary for MongoDB
    expense_dict = expense_data.model_dump(mode='json')
    
    result = collection.insert_one(expense_dict)
    
    client.close()
    
    return str(result.inserted_id)

