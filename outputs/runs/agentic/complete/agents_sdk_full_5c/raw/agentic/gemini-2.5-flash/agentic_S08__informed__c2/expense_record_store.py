import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from document_models import NormalizedExpense

def persist_expense_record(expense: NormalizedExpense, collection_name: str = "expenses") -> str:
    mongodb_uri = os.environ.get("MONGODB_ATLAS_URI")
    if not mongodb_uri:
        raise ValueError("MONGODB_ATLAS_URI environment variable not set.")

    database_name = os.environ.get("MONGODB_DATABASE_NAME", "document_extraction_db")

    try:
        client = MongoClient(mongodb_uri)
        client.admin.command('ping') # Test connection

        db = client[database_name]
        collection = db[collection_name]

        # Convert Pydantic model to dictionary for MongoDB
        expense_dict = expense.model_dump(by_alias=True)

        result = collection.insert_one(expense_dict)
        return str(result.inserted_id)
    except ConnectionFailure as e:
        print(f"MongoDB connection failed: {e}")
        raise
    except OperationFailure as e:
        print(f"MongoDB operation failed: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred during persistence: {e}")
        raise

if __name__ == '__main__':
    # Example usage:
    # from document_models import NormalizedExpense, LineItem
    # expense_data = NormalizedExpense(
    #     vendor="Cloud Services Inc.",
    #     date="2023-11-20",
    #     amount=500.00,
    #     currency="USD",
    #     description="Monthly cloud hosting.",
    #     line_items=[LineItem(description="Server usage", amount=400.0), LineItem(description="Storage", amount=100.0)]
    # )
    #
    # try:
    #     inserted_id = persist_expense_record(expense_data, collection_name="test_expenses")
    #     print(f"Expense record inserted with ID: {inserted_id}")
    # except Exception as e:
    #     print(f"Failed to persist expense record: {e}")
    pass
