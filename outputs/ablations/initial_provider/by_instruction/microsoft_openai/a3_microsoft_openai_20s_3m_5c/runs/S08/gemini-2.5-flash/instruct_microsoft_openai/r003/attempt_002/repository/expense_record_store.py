from document_client import get_mongodb_client
from document_models import NormalizedExpense
from pymongo.results import InsertOneResult

def store_expense_record(expense_record: NormalizedExpense) -> InsertOneResult:
    client = get_mongodb_client()
    db = client.expense_database # Use a specific database
    collection = db.expense_records # Use a specific collection
    
    # Convert Pydantic model to dictionary for MongoDB
    expense_dict = expense_record.model_dump()
    
    result = collection.insert_one(expense_dict)
    client.close()
    return result
