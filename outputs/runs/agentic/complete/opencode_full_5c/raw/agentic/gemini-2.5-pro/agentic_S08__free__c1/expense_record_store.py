import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from document_models import NormalizedExpense


def store_expense_record(expense: NormalizedExpense):
    """
    Stores a normalized expense record in MongoDB Atlas.
    """
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        raise ValueError("MONGO_URI environment variable not set for MongoDB Atlas.")

    try:
        client = MongoClient(mongo_uri)
        db = client.get_default_database()  # The database is usually part of the URI
        if db is None:
            db = client["expenses"]

        collection = db["expense_records"]

        # Validate connection
        client.admin.command("ping")

        expense_dict = expense.dict()
        collection.insert_one(expense_dict)

    except ConnectionFailure as e:
        raise Exception(f"Could not connect to MongoDB: {e}") from e
    except Exception as e:
        raise Exception(
            f"An error occurred while storing the expense record: {e}"
        ) from e
    finally:
        if "client" in locals() and client:
            client.close()
