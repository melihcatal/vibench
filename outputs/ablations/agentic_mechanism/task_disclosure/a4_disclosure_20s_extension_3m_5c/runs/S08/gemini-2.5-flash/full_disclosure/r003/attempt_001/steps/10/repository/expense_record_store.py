from google.cloud import firestore

class ExpenseRecordStore:
    def __init__(self, collection_name="expense_records"):
        self.db = firestore.Client()
        self.collection_ref = self.db.collection(collection_name)

    def save_expense_record(self, record: dict):
        """
        Persists a normalized expense record to Firestore.
        """
        try:
            doc_ref = self.collection_ref.add(record)
            return doc_ref[1].id
        except Exception as e:
            print(f"Error saving expense record: {e}")
            raise