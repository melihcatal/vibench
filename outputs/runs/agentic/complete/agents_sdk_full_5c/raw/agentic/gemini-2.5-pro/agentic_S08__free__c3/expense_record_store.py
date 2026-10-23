import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import ConnectionFailure, OperationFailure

from document_models import NormalizedExpense


def store_expense_record(expense: NormalizedExpense) -> str:
    """
    Persists a normalized expense record into a MongoDB Atlas collection.

    :param expense: The NormalizedExpense object to store.
    :return: The string ID of the inserted MongoDB document.
    """
    mongo_uri = os.environ.get("MONGODB_ATLAS_URI")
    if not mongo_uri:
        raise ValueError("MONGODB_ATLAS_URI environment variable not set.")

    db_name = "expenses"
    collection_name = "normalized_records"

    # Using the recommended ServerApi for compatibility
    client = MongoClient(mongo_uri, server_api=ServerApi('1'))

    try:
        # The ismaster command is cheap and does not require auth.
        client.admin.command('ismaster')
        print("MongoDB Atlas connection successful.")
    except ConnectionFailure as e:
        print(f"MongoDB Atlas connection failed: {e}")
        raise

    db = client[db_name]
    collection = db[collection_name]

    try:
        expense_dict = expense.model_dump()
        result = collection.insert_one(expense_dict)
        print(f"Successfully inserted expense record with ID: {result.inserted_id}")
        return str(result.inserted_id)
    except OperationFailure as e:
        print(f"Failed to insert document into MongoDB: {e}")
        raise
    finally:
        client.close()
