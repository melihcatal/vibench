import os
from pymongo import MongoClient
from document_models import NormalizedExpense, PersistenceResult


def expense_record_store(expense_record: NormalizedExpense) -> PersistenceResult:
    """
    Persists normalized expense records in a MongoDB Atlas document store.
    """
    mongo_uri = os.getenv("MONGO_ATLAS_URI")
    if not mongo_uri:
        raise ValueError("MONGO_ATLAS_URI environment variable not set.")

    client = MongoClient(mongo_uri)
    db = client.get_default_database()  # Assumes database is in the URI
    if db is None:
        db = client["expense_db"]  # Fallback database name

    collection = db["expenses"]

    result = collection.insert_one(expense_record.model_dump())

    return PersistenceResult(
        record_id=str(result.inserted_id),
        success=result.acknowledged,
    )
