import os
import pymongo
from document_models import NormalizedExpense


def get_db_client():
    """Returns a MongoDB client connected to Atlas."""
    mongo_uri = os.getenv("MONGODB_ATLAS_URI")
    if not mongo_uri:
        raise ValueError("MONGODB_ATLAS_URI environment variable not set.")

    client = pymongo.MongoClient(mongo_uri)
    return client


def expense_record_store(
    expense: NormalizedExpense,
    db_name: str = "expenses",
    collection_name: str = "records",
):
    """
    Persists a normalized expense record in MongoDB Atlas.
    """
    client = get_db_client()
    db = client[db_name]
    collection = db[collection_name]

    expense_dict = expense.model_dump()

    result = collection.insert_one(expense_dict)

    return str(result.inserted_id)
