
from google.cloud import firestore

class ExpenseRecordStore:
    def __init__(self, project_id: str, collection_name: str = "expense_records"):
        self.db = firestore.Client(project=project_id)
        self.collection_ref = self.db.collection(collection_name)

    def add_expense_record(self, record: dict):
        """
        Adds a new expense record to the Firestore collection.
        Args:
            record: A dictionary representing the expense record.
                    Example: {"amount": 50.00, "category": "food", "date": "2026-09-20"}
        Returns:
            The ID of the added document.
        """
        try:
            doc_ref = self.collection_ref.add(record)
            return doc_ref[1].id
        except Exception as e:
            print(f"Error adding expense record: {e}")
            return None

# Example usage (assuming GOOGLE_APPLICATION_CREDENTIALS environment variable is set or configured)
# if __name__ == "__main__":
#     # Replace "your-google-cloud-project-id" with your actual Google Cloud Project ID
#     store = ExpenseRecordStore(project_id="your-google-cloud-project-id")
#     
#     new_expense = {
#         "amount": 75.50,
#         "category": "transport",
#         "date": "2026-09-20",
#         "description": "Bus ticket"
#     }
#     
#     record_id = store.add_expense_record(new_expense)
#     if record_id:
#         print(f"Expense record added with ID: {record_id}")
#     else:
#         print("Failed to add expense record.")
