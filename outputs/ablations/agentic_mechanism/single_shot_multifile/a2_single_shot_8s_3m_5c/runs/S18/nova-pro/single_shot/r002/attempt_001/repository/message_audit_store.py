from google.cloud import firestore

db = firestore.Client()

def store_message(message_id, message_data):
    doc_ref = db.collection('messages').document(message_id)
    doc_ref.set(message_data)