from google.cloud import firestore

class MessageAuditStore:
    def __init__(self):
        self.db = firestore.Client()
        self.collection_ref = self.db.collection('message_audit_records')

    def add_message_record(self, record: dict):
        try:
            doc_ref = self.collection_ref.add(record)
            return doc_ref[1].id
        except Exception as e:
            raise RuntimeError(f"Error adding record to Firestore: {e}")
