"""
Persist normalized expense records in a managed document store.
"""
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dataclasses import asdict

from document_models import NormalizedExpense

def store_expense_record(expense: NormalizedExpense):
    """
    Stores a normalized expense record in MongoDB Atlas.
    """
    uri = os.environ.get("MONGODB_ATLAS_URI")
    if not uri:
        raise ValueError("MONGODB_ATLAS_URI environment variable is not set.")

    client = MongoClient(uri)

    try:
        # The ismaster command is cheap and does not require auth.
        client.admin.command('ismaster')
    except ConnectionFailure:
        print("MongoDB Atlas server not available")
        return None

    db = client.expense_data
    collection = db.normalized_expenses

    expense_dict = asdict(expense)
    
    # Insert the document
    result = collection.insert_one(expense_dict)
    
    print(f"Successfully inserted expense record with ID: {result.inserted_id}")
    client.close()
    return result.inserted_id
