from google.cloud import firestore

def conditional_update(document_id, new_value):
    db = firestore.Client()
    doc_ref = db.collection('my-collection').document(document_id)

    @firestore.transactional
    def update_in_transaction(transaction, doc_ref, new_value):
        snapshot = doc_ref.get(transaction=transaction)
        if snapshot.exists:
            current_version = snapshot.get('version')
            updated_data = {
                'value': new_value,
                'version': current_version + 1,
                'updated_by_provider': 'Google Cloud Firestore'
            }
            transaction.update(doc_ref, updated_data)
            print(f"Document {document_id} updated to version {current_version + 1}")
        else:
            initial_data = {
                'value': new_value,
                'version': 1,
                'updated_by_provider': 'Google Cloud Firestore'
            }
            transaction.set(doc_ref, initial_data)
            print(f"Document {document_id} created with version 1")

    transaction = db.transaction()
    update_in_transaction(transaction, doc_ref, new_value)

if __name__ == '__main__':
    # Example usage:
    # Ensure you have Google Cloud authentication set up (e.g., GOOGLE_APPLICATION_CREDENTIALS)
    # python -c "from conditional_update import conditional_update; conditional_update('my-document', 'initial value')"
    # python -c "from conditional_update import conditional_update; conditional_update('my-document', 'updated value')"
    # python -c "from conditional_update import conditional_update; conditional_update('another-document', 'hello world')"
    pass
