import os
from pymongo.results import InsertOneResult
from document_client import get_mongodb_client
from document_models import NormalizedExpense

def persist_expense_record(expense_record: NormalizedExpense) -> InsertOneResult:
    client = get_mongodb_client()
    
    db_name = os.getenv("MONGO_DB_NAME", "expense_db")
    collection_name = os.getenv("MONGO_COLLECTION_NAME", "expenses")

    db = client[db_name]
    collection = db[collection_name]

    # Convert Pydantic model to dictionary for MongoDB insertion
    expense_dict = expense_record.model_dump(by_alias=True)

    result = collection.insert_one(expense_dict)
    return result
