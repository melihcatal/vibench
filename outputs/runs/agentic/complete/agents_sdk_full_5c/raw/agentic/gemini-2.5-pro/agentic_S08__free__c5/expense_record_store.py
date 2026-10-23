# expense_record_store.py
from document_client import get_mongo_collection
from document_models import NormalizedExpense

def save_expense_record(expense: NormalizedExpense) -> str:
    """
    Saves a normalized expense record to a MongoDB Atlas collection.

    :param expense: The NormalizedExpense object to save.
    :return: The string representation of the inserted document's ID.
    """
    collection = get_mongo_collection()
    
    # Pydantic model needs to be converted to a dict for pymongo
    expense_dict = expense.model_dump()
    
    result = collection.insert_one(expense_dict)
    
    return str(result.inserted_id)
