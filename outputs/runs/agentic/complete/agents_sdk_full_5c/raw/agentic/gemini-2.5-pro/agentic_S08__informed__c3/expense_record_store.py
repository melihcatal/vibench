import os
from dataclasses import asdict
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from document_models import NormalizedExpense

def get_db_collection():
    """
    Connects to MongoDB Atlas and returns the expense records collection.
    """
    uri = os.environ.get("MONGODB_ATLAS_URI")
    if not uri:
        raise ValueError("MONGODB_ATLAS_URI environment variable not found.")

    client = MongoClient(uri)
    
    try:
        # The ismaster command is cheap and does not require auth.
        client.admin.command('ismaster')
    except ConnectionFailure:
        raise Exception("MongoDB Atlas server not available")

    db = client.get_database("expenses_db")
    return db.get_collection("records")

def store_expense_record(expense: NormalizedExpense) -> str:
    """
    Persists a normalized expense record in MongoDB Atlas.
    Returns the ID of the inserted document.
    """
    collection = get_db_collection()
    expense_dict = asdict(expense)
    result = collection.insert_one(expense_dict)
    return str(result.inserted_id)
