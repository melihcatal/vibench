import os
from pymongo import MongoClient
from document_models import NormalizedExpense


def store_expense_record(expense_record: NormalizedExpense):
    connection_string = os.environ.get("MONGODB_ATLAS_URI")
    if not connection_string:
        raise ValueError("MONGODB_ATLAS_URI environment variable not set.")

    client = MongoClient(connection_string)
    db = client.get_database("expense_db")
    collection = db.get_collection("expenses")

    record_dict = expense_record.dict()

    result = collection.insert_one(record_dict)

    return str(result.inserted_id)
