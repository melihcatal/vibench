import os
from google.cloud import firestore

class ExpenseRecordStore:
    def __init__(self, project_id: str, collection_name: str = "expense_records"):
        os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
        self.db = firestore.Client()
        self.collection_ref = self.db.collection(collection_name)

    def save_expense_record(self, record: dict) -> str:
        """
        Persists a normalized expense record in Google Cloud Firestore.

        Args:
            record (dict): The normalized expense record to save.

        Returns:
            str: The ID of the created document in Firestore.
        """
        doc_ref = self.collection_ref.add(record)
        return doc_ref[1].id
