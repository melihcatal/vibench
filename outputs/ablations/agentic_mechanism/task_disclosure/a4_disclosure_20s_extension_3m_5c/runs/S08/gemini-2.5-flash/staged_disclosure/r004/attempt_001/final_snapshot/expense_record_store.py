from google.cloud import firestore

class ExpenseRecordStore:
    def __init__(self, project_id: str):
        self.db = firestore.Client(project=project_id)
        self.collection_ref = self.db.collection('expense_records')

    def save_expense_record(self, record: dict) -> str:
        """
        Persists a normalized expense record in Google Cloud Firestore.
        Args:
            record: A dictionary representing the normalized expense record.
        Returns:
            The ID of the saved document.
        """
        doc_ref = self.collection_ref.add(record)
        return doc_ref[1].id

