from google.cloud import firestore


def store_expense_record(expense_record):
    db = firestore.Client()
    doc_ref = db.collection('expenses').document()
    doc_ref.set(expense_record)
    return doc_ref.id