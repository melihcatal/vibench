import os
from pymongo import MongoClient
from document_models import NormalizedExpense


def store_expense_record(expense: NormalizedExpense):
    """
    Persists a normalized expense record in a MongoDB Atlas collection.
    """
    mongo_uri = os.environ.get("MONGODB_ATLAS_URI")
    if not mongo_uri:
        raise ValueError("MONGODB_ATLAS_URI environment variable must be set.")

    client = MongoClient(mongo_uri)

    try:
        db = client.get_database("expenses")
        collection = db.get_collection("normalized_records")

        expense_dict = expense.model_dump()
        result = collection.insert_one(expense_dict)

        return str(result.inserted_id)
    except Exception as e:
        # In a real app, you'd want more robust error handling
        print(f"Error connecting to or writing to MongoDB: {e}")
        return None
    finally:
        client.close()
