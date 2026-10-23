import firebase_admin
from firebase_admin import credentials, firestore

# Firestore NoSQL store (later-step)
cred = credentials.Certificate(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
firebase_admin.initialize_app(cred)


def store_expense_record(normalized_json):
    db = firestore.client()
    doc_ref = db.collection("expenses").document()
    doc_ref.set(json.loads(normalized_json))
    return doc_ref.id
