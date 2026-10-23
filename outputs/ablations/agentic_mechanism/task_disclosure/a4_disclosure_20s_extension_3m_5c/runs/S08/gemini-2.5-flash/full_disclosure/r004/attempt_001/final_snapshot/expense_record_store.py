from google.cloud import firestore

class ExpenseRecordStore:
    def __init__(self, project_id: str):
        self.db = firestore.Client(project=project_id)
        self.collection_ref = self.db.collection('expense_records')

    def persist_expense_record(self, record: dict):
        """
        Persists a normalized expense record to Firestore.
        """
        try:
            doc_ref = self.collection_ref.add(record)
            return doc_ref[1].id
        except Exception as e:
            print(f"Error persisting expense record: {e}")
            raise

