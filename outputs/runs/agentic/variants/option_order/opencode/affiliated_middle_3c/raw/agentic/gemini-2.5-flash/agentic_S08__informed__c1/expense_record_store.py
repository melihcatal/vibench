import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure


def persist_expense_record(
    record: dict, collection_name: str = "expense_records"
) -> str:
    """
    Persists normalized expense records in a managed MongoDB Atlas document store.
    """
    mongo_uri = os.environ.get("MONGODB_ATLAS_URI")
    if not mongo_uri:
        raise ValueError("MONGODB_ATLAS_URI environment variable not set.")

    try:
        client = MongoClient(mongo_uri)
        db = (
            client.get_database()
        )  # Connects to the default database specified in the URI, or 'admin' if none.
        collection = db[collection_name]

        insert_result = collection.insert_one(record)
        return str(insert_result.inserted_id)
    except ConnectionFailure as e:
        raise ConnectionFailure(f"Could not connect to MongoDB Atlas: {e}")
    except OperationFailure as e:
        raise OperationFailure(f"MongoDB operation failed: {e}")
    finally:
        if "client" in locals() and client:
            client.close()


if __name__ == "__main__":
    # Placeholder for actual usage with MONGODB_ATLAS_URI set
    if not os.environ.get("MONGODB_ATLAS_URI"):
        print("Please set MONGODB_ATLAS_URI environment variable.")
    else:
        sample_expense_record = {
            "transaction_type": "invoice",
            "vendor_name": "Tech Solutions",
            "transaction_date": "2024-04-19",
            "total_amount": 99.99,
            "currency": "USD",
            "line_items": [
                {
                    "description": "Software License",
                    "quantity": 1,
                    "unit_price": 99.99,
                    "total_price": 99.99,
                }
            ],
            "raw_extracted_data": {"source": "Document AI", "original_text": "..."},
        }
        try:
            # record_id = persist_expense_record(sample_expense_record)
            # print(f"Expense record persisted with ID: {record_id}")
            print("MongoDB Atlas client configured for expense record storage.")
        except (ConnectionFailure, OperationFailure) as e:
            print(f"Error during MongoDB operation: {e}")
