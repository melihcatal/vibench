from google.cloud import firestore

def conditional_update(document_id, update_data, condition):
    db = firestore.Client()
    doc_ref = db.collection(u'documents').document(document_id)
    doc = doc_ref.get()
    if doc.exists and doc.to_dict().get('version') == condition:
        doc_ref.update(update_data)
        print(f'Document {document_id} updated successfully with condition {condition}')
    else:
        print(f'Document {document_id} does not meet the condition {condition}')