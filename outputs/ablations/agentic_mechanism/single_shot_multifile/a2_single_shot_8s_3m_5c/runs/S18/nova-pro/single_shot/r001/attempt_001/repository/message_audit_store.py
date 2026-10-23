from google.cloud import firestore

db = firestore.Client()

def store_message_record(message_id, message_data):
    doc_ref = db.collection('message_audit').document(message_id)
    doc_ref.set(message_data)