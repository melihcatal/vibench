import os
from dataclasses import asdict
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from document_models import Expense


def store_expense_record(expense: Expense):
    """
    Persists a normalized expense record in a MongoDB Atlas database.
    """
    uri = os.getenv("MONGODB_ATLAS_URI")
    if not uri:
        raise ValueError("MONGODB_ATLAS_URI environment variable is not set.")

    client = None
    try:
        client = MongoClient(uri, server_api=ServerApi("1"))
        db = client.expense_database
        collection = db.expense_records

        expense_dict = asdict(expense)

        # Convert date to a MongoDB-friendly format if needed, though string is fine
        # For more advanced queries, converting to datetime object would be better
        # expense_dict['date'] = datetime.fromisoformat(expense.date)

        result = collection.insert_one(expense_dict)
        return result.inserted_id
    except Exception as e:
        print(f"An error occurred while storing the expense record: {e}")
        return None
    finally:
        if client:
            client.close()
