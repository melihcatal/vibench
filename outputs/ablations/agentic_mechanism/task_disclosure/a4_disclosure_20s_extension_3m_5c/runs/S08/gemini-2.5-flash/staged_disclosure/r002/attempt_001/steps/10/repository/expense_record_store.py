from google.cloud import firestore

class ExpenseRecordStore:
    def __init__(self, project_id: str):
        self.db = firestore.Client(project=project_id)
        self.collection_ref = self.db.collection('expense_records')

    def add_expense_record(self, record: dict):
        """
        Adds a new expense record to Firestore.
        The record dictionary should contain normalized expense data.
        """
        doc_ref = self.collection_ref.document()
        doc_ref.set(record)
        return doc_ref.id

    def get_expense_record(self, record_id: str):
        """
        Retrieves an expense record by its ID.
        """
        doc = self.collection_ref.document(record_id).get()
        if doc.exists:
            return doc.to_dict()
        else:
            return None

    def update_expense_record(self, record_id: str, updates: dict):
        """
        Updates an existing expense record.
        """
        doc_ref = self.collection_ref.document(record_id)
        doc_ref.update(updates)

    def delete_expense_record(self, record_id: str):
        """
        Deletes an expense record.
        """
        self.collection_ref.document(record_id).delete()

