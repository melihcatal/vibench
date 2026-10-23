import google.cloud.firestore as firestore

def conditional_update(collection_name, document_id, update_data, condition):
    db = firestore.Client()
    doc_ref = db.collection(collection_name).document(document_id)
    try:
        doc_ref.update(update_data, condition)
    except Exception as e:
        print(f"Update failed: {e}")