from google.cloud import firestore

def fetch_document(document_id):
    db = firestore.Client()
    doc_ref = db.collection(u'documents').document(document_id)
    doc = doc_ref.get()
    if doc.exists:
        print(f'Document {document_id} fetched successfully: {doc.to_dict()}')
    else:
        print(f'Document {document_id} does not exist.')