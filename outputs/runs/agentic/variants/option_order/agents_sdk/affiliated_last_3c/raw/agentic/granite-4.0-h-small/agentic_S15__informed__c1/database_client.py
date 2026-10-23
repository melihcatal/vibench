import json

class FirestoreDocument:
    def __init__(self, client):
        self.client = client

    def upsert_document(self, collection, doc_id, data):
        doc_ref = self.client.collection(collection).document(doc_id)
        doc_ref.set(data)

    def fetch_document(self, collection, doc_id):
        doc_ref = self.client.collection(collection).document(doc_id)
        doc = doc_ref.get()
        return doc.to_dict() if doc.exists else None

    def query_documents(self, collection, field, value):
        query = self.client.collection(collection).where(field, '==', value)
        results = query.stream()
        return [doc.to_dict() for doc in results]

    def conditional_update(self, collection, doc_id, update_fields, condition_field, condition_value):
        doc_ref = self.client.collection(collection).document(doc_id)
        doc_ref.update(update_fields, {'ifExists': True})  # Firestore does not support native conditionals; implement via transaction if needed