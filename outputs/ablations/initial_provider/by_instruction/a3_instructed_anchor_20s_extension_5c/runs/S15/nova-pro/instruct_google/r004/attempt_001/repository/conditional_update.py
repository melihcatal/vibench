import google.cloud.firestore as firestore

def conditional_update(document_id, update_data, condition):
    db = firestore.Client()
    doc_ref = db.collection(u'documents').document(document_id)
    doc_ref.update(update_data, condition)