import os
from typing import Dict, Any
from pymongo import MongoClient
from document_models import NormalizedExpense

class ExpenseRecordStore:
    """
    Persists normalized expense records in Azure Cosmos DB (MongoDB API).
    """
    def __init__(self):
        self.connection_string = os.environ.get("COSMOS_CONNECTION_STRING")
        self.database_name = os.environ.get("COSMOS_DATABASE_NAME", "expense_db")
        self.collection_name = os.environ.get("COSMOS_COLLECTION_NAME", "expense_records")

        if not self.connection_string:
            raise ValueError("COSMOS_CONNECTION_STRING must be set in environment variables.")

        self.client = MongoClient(self.connection_string)
        self.db = self.client[self.database_name]
        self.collection = self.db[self.collection_name]

    def save_expense(self, expense_record: NormalizedExpense) -> Dict[str, Any]:
        """
        Saves a normalized expense record to the Cosmos DB collection.
        """
        # Convert dataclass to a dictionary for MongoDB insertion
        expense_dict = expense_record.__dict__
        # Convert nested dataclasses (like LineItem) to dictionaries as well
        expense_dict["line_items"] = [item.__dict__ for item in expense_record.line_items]

        try:
            result = self.collection.insert_one(expense_dict)
            print(f"Expense record saved with ID: {result.inserted_id}")
            return {"status": "success", "inserted_id": str(result.inserted_id)}
        except Exception as e:
            print(f"Error saving expense record: {e}")
            return {"status": "error", "message": str(e)}

    def close_connection(self):
        """
        Closes the MongoDB client connection.
        """
        if self.client:
            self.client.close()
