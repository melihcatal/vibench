from google.cloud import firestore

def persist_expense_record(expense: dict):
    client = firestore.Client()
    doc_ref = client.collection(u"expenses").document()
    doc_ref.set(expense)