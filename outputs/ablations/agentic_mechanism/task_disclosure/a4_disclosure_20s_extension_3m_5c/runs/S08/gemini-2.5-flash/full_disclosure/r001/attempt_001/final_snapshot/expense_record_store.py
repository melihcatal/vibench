from google.cloud import firestore
import os

class ExpenseRecordStore:
    def __init__(self, collection_name="expense_records"):
        # Initialize Firestore client
        # It's assumed that GOOGLE_APPLICATION_CREDENTIALS environment variable
        # is set or running in a Google Cloud environment.
        self.db = firestore.Client()
        self.collection_ref = self.db.collection(collection_name)

    def persist_expense_record(self, record: dict) -> str:
        """
        Persists a normalized expense record to Firestore.

        Args:
            record (dict): The normalized expense record to store.

        Returns:
            str: The ID of the created document in Firestore.
        """
        try:
            doc_ref = self.collection_ref.add(record)
            return doc_ref[1].id
        except Exception as e:
            print(f"Error persisting expense record: {e}")
            raise