from google.cloud import firestore

def store_message_record(message_id: str, data: dict):
    """
    Persists a processed message record to Google Cloud Firestore for later lookup.

    Args:
        message_id: The unique ID of the processed message.
        data: A dictionary containing the message record data to store.
    """
    db = firestore.Client()
    doc_ref = db.collection('message_audit_records').document(message_id)
    doc_ref.set(data)
