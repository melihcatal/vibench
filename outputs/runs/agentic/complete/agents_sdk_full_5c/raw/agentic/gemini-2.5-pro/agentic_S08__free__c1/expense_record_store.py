from document_client import get_mongo_client
from document_models import NormalizedExpense
from pymongo.results import InsertOneResult

def persist_expense_record(expense: NormalizedExpense) -> InsertOneResult:
    """
    Persists a normalized expense record into a MongoDB Atlas collection.
    
    Assumes a database named 'expenses_db' and a collection 'records'.
    """
    client = get_mongo_client()
    db = client.get_database("expenses_db")
    collection = db.get_collection("records")
    
    # Using the Pydantic model's dict representation for insertion
    expense_dict = expense.model_dump()
    
    # In a real application, you might add metadata like insertion timestamp
    # from datetime import datetime, timezone
    # expense_dict['createdAt'] = datetime.now(timezone.utc)
    
    result = collection.insert_one(expense_dict)
    
    return result

