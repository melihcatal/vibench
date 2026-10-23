import os
from pymongo import MongoClient
from document_models import NormalizedExpense


def store_expense_record(expense_record: NormalizedExpense):
    """
    Persists normalized expense records in a MongoDB Atlas document store.
    """
    connection_string = os.getenv("MONGO_ATLAS_CONNECTION_STRING")
    if not connection_string:
        raise ValueError("MongoDB Atlas connection string is not set.")

    client = MongoClient(connection_string)
    db = client.get_default_database()  # Assumes database is in connection string

    expenses_collection = db["expenses"]

    record_dict = expense_record.dict()

    result = expenses_collection.insert_one(record_dict)

    return str(result.inserted_id)
