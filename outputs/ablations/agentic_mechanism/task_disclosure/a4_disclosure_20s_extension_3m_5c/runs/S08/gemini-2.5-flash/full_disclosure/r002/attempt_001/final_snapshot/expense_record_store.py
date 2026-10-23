from google.cloud import firestore
import os

class ExpenseRecordStore:
    def __init__(self, project_id: str = None):
        if project_id is None:
            # Attempt to get project ID from environment variable if not provided
            project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
            if not project_id:
                raise ValueError("Google Cloud Project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable.")
        
        self.db = firestore.Client(project=project_id)
        self.collection_name = "expense_records"

    def save_expense_record(self, record: dict):
        """
        Persists a normalized expense record to Firestore.
        
        Args:
            record: A dictionary representing the normalized expense record.
        """
        try:
            doc_ref = self.db.collection(self.collection_name).document()
            doc_ref.set(record)
            return {"status": "success", "id": doc_ref.id}
        except Exception as e:
            return {"status": "error", "message": str(e)}
