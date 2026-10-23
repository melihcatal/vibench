import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from document_models import NormalizedExpense


def expense_record_store(expense_record: NormalizedExpense):
    """
    Persists a normalized expense record in a MongoDB Atlas document store.
    """
    connection_string = os.environ.get("MONGO_ATLAS_CONNECTION_STRING")
    if not connection_string:
        raise ValueError("MONGO_ATLAS_CONNECTION_STRING environment variable not set.")

    try:
        client = MongoClient(connection_string)
        # The ismaster command is cheap and does not require auth.
        client.admin.command("ismaster")
    except ConnectionFailure as e:
        raise ConnectionFailure(f"Could not connect to MongoDB Atlas: {e}") from e

    db = client.expense_database
    collection = db.normalized_expenses

    try:
        result = collection.insert_one(expense_record.dict())
        return result.inserted_id
    finally:
        client.close()
