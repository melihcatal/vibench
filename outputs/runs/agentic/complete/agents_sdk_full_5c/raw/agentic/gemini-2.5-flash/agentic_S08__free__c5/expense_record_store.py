import os
from typing import Dict, Any
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from document_models import ExpenseRecord
from document_client import load_config
from bson.objectid import ObjectId

def persist_expense_record(record: ExpenseRecord) -> Dict[str, Any]:
    """
    Persists normalized expense records in a managed document store (MongoDB Atlas).
    """
    config = load_config("mongodb")
    connection_string = config.get("connection_string")
    database_name = config.get("database_name")
    collection_name = config.get("collection_name")

    if not all([connection_string, database_name, collection_name]):
        raise ValueError("MongoDB connection details (connection_string, database_name, collection_name) must be set in environment variables.")

    try:
        # Connect to MongoDB Atlas
        client = MongoClient(connection_string)
        client.admin.command('ping') # Test connection
        db = client[database_name]
        collection = db[collection_name]

        # Convert ExpenseRecord Pydantic model to a dictionary for MongoDB
        record_dict = record.model_dump(by_alias=True, exclude_none=True)

        # If record_id is present and valid ObjectId, try to update; otherwise, insert.
        if record.record_id and ObjectId.is_valid(record.record_id):
            object_id = ObjectId(record.record_id)
            result = collection.update_one({'_id': object_id}, {'$set': record_dict}, upsert=True)
            if result.upserted_id:
                record_id_str = str(result.upserted_id)
                action = "inserted"
            else:
                record_id_str = record.record_id
                action = "updated"
        else:
            result = collection.insert_one(record_dict)
            record_id_str = str(result.inserted_id)
            action = "inserted"
        
        # Close the connection
        client.close()

        return {
            "status": "success",
            "action": action,
            "record_id": record_id_str,
            "message": f"Expense record {record_id_str} {action} successfully."
        }
    except ConnectionFailure as e:
        return {"status": "error", "message": f"MongoDB Connection Error: {e}"}
    except OperationFailure as e:
        return {"status": "error", "message": f"MongoDB Operation Error: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"An unexpected error occurred: {e}"}

if __name__ == '__main__':
    from datetime import date
    from document_models import LineItem

    # !!! IMPORTANT: Replace with your actual MongoDB Atlas connection string and details !!!
    os.environ["MONGODB_CONNECTION_STRING"] = "mongodb+srv://<user>:<password>@<cluster-url>/<database>?retryWrites=true&w=majority"
    os.environ["MONGODB_DATABASE_NAME"] = "expense_db"
    os.environ["MONGODB_COLLECTION_NAME"] = "expense_records"

    # Example ExpenseRecord to persist
    sample_expense = ExpenseRecord(
        document_type="invoice",
        vendor_name="Office Supplies Co.",
        transaction_date="2023-11-01",
        total_amount=250.75,
        tax_amount=15.25,
        currency="USD",
        line_items=[
            LineItem(description="Pens", quantity=5.0, unit_price=2.50, amount=12.50),
            LineItem(description="Notebooks", quantity=10.0, unit_price=5.00, amount=50.00)
        ],
        notes="Monthly office replenishment.",
        validation_status={"is_valid": True, "missing_fields": []},
        summary="Summary of office supplies invoice from Office Supplies Co. totaling 250.75 USD for pens and notebooks."
    )

    print("Attempting to persist sample expense record...")
    try:
        result = persist_expense_record(sample_expense)
        print("Persistence Result:", result)

        # Example of updating an existing record (if record_id is set)
        # If you run the above once, you can uncomment and run this with the printed record_id
        # sample_expense.record_id = result.get("record_id")
        # sample_expense.total_amount = 260.00 # Modify a field
        # update_result = persist_expense_record(sample_expense)
        # print("\nUpdate Result:", update_result)

    except ValueError as ve:
        print(f"Configuration Error: {ve}")
    except Exception as e:
        print(f"Failed to persist expense record: {e}")

    print("\nTo run, ensure MONGODB_CONNECTION_STRING, MONGODB_DATABASE_NAME, and MONGODB_COLLECTION_NAME environment variables are set with your MongoDB Atlas details.")
