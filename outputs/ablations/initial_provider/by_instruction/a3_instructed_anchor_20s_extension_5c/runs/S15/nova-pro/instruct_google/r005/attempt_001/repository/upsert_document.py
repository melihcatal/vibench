from google.cloud import firestore

def upsert_document(document_id, document_data):
    db = firestore.Client()
    doc_ref = db.collection(u'documents').document(document_id)
    doc_ref.set(document_data)
    print(f'Document {document_id} upserted successfully.')