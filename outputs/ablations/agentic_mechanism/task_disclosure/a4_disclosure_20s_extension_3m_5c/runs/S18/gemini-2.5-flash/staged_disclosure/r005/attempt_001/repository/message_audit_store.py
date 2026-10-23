from google.cloud import firestore

class MessageAuditStore:
    def __init__(self, project_id: str, collection_name: str = "message_audits"):
        self.db = firestore.Client(project=project_id)
        self.collection_ref = self.db.collection(collection_name)

    def save_message(self, message_id: str, message_content: dict):
        doc_ref = self.collection_ref.document(message_id)
        doc_ref.set(message_content)
        return True

    def get_message(self, message_id: str):
        doc_ref = self.collection_ref.document(message_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return None

