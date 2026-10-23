import os
from pymongo import MongoClient
from document_models import NormalizedExpense


def expense_record_store(expense: NormalizedExpense):
    connection_string = os.environ.get("MONGODB_ATLAS_URI")
    if not connection_string:
        raise ValueError("MONGODB_ATLAS_URI environment variable not set")

    client = MongoClient(connection_string)
    db = client.get_database("expense_reports")
    collection = db.get_collection("normalized_expenses")

    expense_dict = expense.dict()

    result = collection.insert_one(expense_dict)

    return str(result.inserted_id)
